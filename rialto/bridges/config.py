import os

from web3 import Web3, HTTPProvider
from sdk.rpc import get_chainid
from ..colors import *
from ..abi import BRIDGE_ABI
from .resource_ids import RESOURCE_IDS

HOME = os.environ['HOME']

class ChainConfig:
    def __init__(self, name, start, confirmations, chainid, url, id, bridge, handler, chainid2, url2, id2, bridge2, handler2):
        self.path = f'{HOME}/.rialto/{name}/{bridge}'
        self.name = name
        self.start = start
        self.confirmations = confirmations
        self.chainid = chainid
        self.chainid2 = chainid2
        self.id = id
        self.id2 = id2
        self.url = url
        self.url2 = url2
        self.bridge = bridge
        self.bridge2 = bridge2
        self.handler = handler
        self.handler2 = handler2
        self.resources = RESOURCE_IDS

    def validate(self):
        if self.chainid != get_chainid(self.url):
            print("{}chainid mismatch, url: {}{}".format(FAIL, self.url, ENDC))
            exit(-1)
        if self.chainid2 != get_chainid(self.url2):
            print("{}chainid2 mismatch, url2: {}{}".format(FAIL, self.url2, ENDC))
            exit(-1)
        return self

    def clean_files(self):
        for f in os.listdir(self.path):
            os.remove(os.path.join(self.path, f))

    def file_deposit(self, mode='a', create=True):
        return self._open_file("deposits.log", mode, create)

    def file_pending(self, mode, create):
        return self._open_file("pending.json", mode, create)

    def file_cancelled(self, mode, create):
        return self._open_file("cancelled.json", mode, create)

    def bridge_contract(self):
        w3 = Web3(HTTPProvider(self.url))
        bridge_address = Web3.toChecksumAddress(self.bridge)
        return w3.eth.contract(address=bridge_address, abi=BRIDGE_ABI)

    def bridge_contract2(self):
        w3 = Web3(HTTPProvider(self.url2))
        bridge_address = Web3.toChecksumAddress(self.bridge2)
        return w3.eth.contract(address=bridge_address, abi=BRIDGE_ABI)

    def _create_path(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def _open_file(self, name, mode, create):
        self._create_path()
        name = os.path.join(self.path, name)
        if os.path.exists(name):
            # read/append/truncate if file already exists
            return open(name, mode)
        elif create:
            # create a new file if not
            return open(name, 'w')
        else:
            # don't create if not asked
            return None
        