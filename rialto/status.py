import json
from rialto.logger import logger
from rialto.bridges.config import ChainConfig
from rialto.deposit import DepositDecoder, ERC20Deposit, DepositEncoder, DepositDecoder
import os.path as path
import sys
sdkpath = path.abspath(path.join(path.dirname(__file__), ".."))
sys.path.append(sdkpath)
from sdk import *

class BridgeStatus:
    def __init__(self, chain: ChainConfig):
        self.chain = chain
        self.from_block = chain.start
        # self.last_block = chain.start
        self.pending_nonces = []      # list of nonces for all pending deposits
        self.pending_deposits = {}    # map {nonce: deposit} of all [Unknown, Active, Passed] deposits
        self.cancelled_deposits = {}  # map {nonce: deposit} of all Cancelled deposits

    def get_pending_deposit(self, nonce):
        if nonce in self.pending_deposits:
            return self.pending_deposits[nonce]
        return None

    def add_pending_deposit(self, deposit: ERC20Deposit):
        if deposit.nonce not in self.pending_deposits:
            self.pending_deposits[deposit.nonce] = deposit
            self.pending_nonces = sorted(self.pending_deposits.keys())

    def del_pending_deposit(self, deposit: ERC20Deposit):
        if deposit.nonce in self.pending_deposits:
            del self.pending_deposits[deposit.nonce]
            self.pending_nonces = sorted(self.pending_deposits.keys())

    def add_cancelled_deposit(self, deposit: ERC20Deposit):
        if deposit.nonce not in self.cancelled_deposits:
            self.cancelled_deposits[deposit.nonce] = deposit

    def get_pending_nonces(self):
        return self.pending_nonces
    
    def load_status(self, latest):
        # start from latest if asked
        if latest:
            self.chain.clean_files()
            self.from_block = get_height_safe(self.chain.url)
            return

        # load from_block
        f_deposit = self.chain.file_deposit('r', create=False)
        if f_deposit:
            try:
                last_line = f_deposit.readlines()[-1]
                self.from_block = int(last_line.split()[2]) + 1
            except:
                pass
        
        # load pending deposits
        f_pending = self.chain.file_pending('r', create=False)
        if f_pending:
            for _nonce, deposit_dict in json.load(f_pending).items():
                deposit = ERC20Deposit.from_dict(deposit_dict)
                self.add_pending_deposit(deposit)
            f_pending.close()

        # load cancelled deposits
        f_cancelled = self.chain.file_cancelled('r', create=False)
        if f_cancelled:
            for _nonce, deposit_dict in json.load(f_cancelled).items():
                deposit = ERC20Deposit.from_dict(deposit_dict)
                self.add_cancelled_deposit(deposit)
            f_cancelled.close()

    def dump_status(self):
        # dump pending deposits order by nonce
        f_pending = self.chain.file_pending('w', create=True)
        pending_deposits = {k: v for k, v in sorted(self.pending_deposits.items())}
        json.dump(pending_deposits, f_pending, indent=4, cls=DepositEncoder)
        f_pending.close()

        # dump cancelled deposits
        f_cancelled = self.chain.file_cancelled('w', create=True)
        cancelled_deposits = {k: v for k, v in sorted(self.cancelled_deposits.items())}
        json.dump(cancelled_deposits, f_cancelled, indent=4, cls=DepositEncoder)
        f_cancelled.close()
