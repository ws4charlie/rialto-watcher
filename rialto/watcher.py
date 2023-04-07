#!/usr/bin/env python3

from rialto.bridges import ChainConfig, is_ERC20
from rialto.deposit import *
from rialto.status import BridgeStatus
from rialto.logger import logger
from datetime import datetime
import subprocess
import os.path as path
import sys
sdkpath = path.abspath(path.join(path.dirname(__file__), ".."))
sys.path.append(sdkpath)
from sdk import *

BATCH_SIZE = 1000

class RialtoWatcher:
    def __init__(self, chain: ChainConfig):
        self.chain = chain
        self.flogs = chain.file_deposit()
        self.bridge = chain.bridge_contract()
        self.bridge2 = chain.bridge_contract2()
        self.status = BridgeStatus(chain)
        self.pending_nonces = []    # list of nonces for all pending deposits
        self.last_checked_nonce = 0 # last nonce (of deposit) checked
        self.next_nonce_2_check = 0 # next (deposit) nonce to check
    
    def load(self, latest):
        self.status.load_status(latest)
        return self

    def watch(self):
        # catch up
        next = self._catch_up(self.status.from_block)

        # start watching
        self._watch_deposits(next)

    def _data_hash(self, amount, recipient, handler, deposit: ERC20Deposit):
        amount = deposit.amount
        recipient = deposit.to
        handler = self.chain.handler2
        out_str = subprocess.check_output(['cb-sol-cli', 'erc20', 'data-hash', '--amount', amount, '--recipient', recipient, '--handler', handler])
        parsed = out_str.split()

    def _check_deposits(self, deadline=3.0):
        bgn = datetime.now()

        # locate the next nonce's position
        pos = 0
        nonces = self.status.get_pending_nonces()
        if self.last_checked_nonce in nonces and self.last_checked_nonce != nonces[-1]:
            pos = nonces.index(self.last_checked_nonce) + 1

        # check pending deposits (order by nonce asc) no more than deadline
        deposits = []
        elapsed = 0.0
        while pos < len(nonces):
            # get the deposit
            nonce = nonces[pos]
            deposit: ERC20Deposit = self.status.get_pending_deposit(nonce)
            status = deposit.status

            # update deposit status
            deposit.update(self.bridge2)
            if deposit.status != status:
                deposits.append(deposit)

            # next position
            pos += 1
            self.last_checked_nonce = nonce

            # continue checking or not
            elapsed = (datetime.now() - bgn).total_seconds()
            if elapsed >= deadline:
                break
            time.sleep(0.2)

        return deposits, elapsed

    def _fetch_deposits(self, block_from, block_to, rest=3.0):
        logs = get_logs_safe(self.chain.url, self.chain.bridge, block_from, block_to, [TOPIC_DEPOSIT])
        deposits = []
        for log in logs:
            rId = log.topics[2].hex()
            tx = get_transaction_safe(self.chain.url, log.transactionHash.hex())
            if is_ERC20(rId):
                deposit = ERC20Deposit.from_log(self.chain, tx, log)
                deposit.update(self.bridge2)
                deposits.append(deposit)
            else:
                height = tx["blockNumber"]
                logger.info(f"{self.chain.name}: block={height} tx={log.transactionHash.hex()}  Unknown resource: {rId}")
        
        # write to log files
        if len(deposits) > 0:
            self._log_deposits(deposits)

    def _watch_deposits(self, block_from, batch=BATCH_SIZE, interval=60.0):
        # get latest height
        latest = get_height_safe(self.chain.url)
        logger.info(f"watching deposits, url={self.chain.url}, height={block_from}, latest={latest}")

        # start watching
        batch_bgn = block_from
        batch_end = min(batch_bgn + batch - 1, latest - self.chain.confirmations)
        while True:
            # fetch new deposits, if any
            if batch_end >= batch_bgn:
                self._fetch_deposits(batch_bgn, batch_end)

            # update pending deposit status, if any
            deposits, elapsed = self._check_deposits(deadline=3.0)

            # write to log files and rest
            if len(deposits) > 0:
                self._log_deposits(deposits)
            if elapsed < interval:
                time.sleep(interval - elapsed)

            # next iteration
            latest = get_height_safe(self.chain.url)
            batch_bgn = batch_end + 1
            batch_end = min(batch_bgn + batch - 1, latest - self.chain.confirmations)

    def _catch_up(self, block_from, batch=BATCH_SIZE):
        # get latest height
        latest = get_height_safe(self.chain.url)
        logger.info(f"catching up... url={self.chain.url}, height={block_from}, latest={latest}")

        # catch up in batches
        batch_bgn = int(block_from)
        batch_end = min(batch_bgn + batch - 1, latest - self.chain.confirmations)
        while batch_end >= batch_bgn:
            self._fetch_deposits(batch_bgn, batch_end)
            latest = get_height_safe(self.chain.url)
            batch_bgn = batch_end + 1
            batch_end = min(batch_bgn + batch - 1, latest - self.chain.confirmations)

            # rest
            time.sleep(1.0)

        # return next block to scan
        return batch_bgn

    def _add_del_watch(self, deposit: ERC20Deposit):
        if deposit.status in [Status.UNKNOWN, Status.ACTIVE, Status.PASSED]:
            self.status.add_pending_deposit(deposit)
        if deposit.status == Status.EXECUTED:
            self.status.del_pending_deposit(deposit)
        if deposit.status == Status.CANCELLED:
            self.status.add_cancelled_deposit(deposit)

    def _log_deposit(self, deposit: ERC20Deposit, flush=True):
        # add/del deposit from watch list
        self._add_del_watch(deposit)

        # write to file
        msg = deposit.format()
        logger.info(msg)

        self.flogs.write(msg + "\n")
        if flush:
            self.flogs.flush()

    def _log_deposits(self, deposits):
        for deposit in deposits:
            self._log_deposit(deposit, flush=False)
        self.status.dump_status()
        self.flogs.flush()
