import json, web3
from collections import namedtuple
from json import JSONEncoder
from enum import IntEnum
from rialto.colors import *
from rialto.bridges import get_symbol, get_decimal, get_proposal_safe

# 0xdbb69440df8433824a026ef190652f29929eb64b4d1d5d2a69be8afe3e6eaed8
TOPIC_DEPOSIT = web3.Web3.solidityKeccak(['bytes'], [b'Deposit(uint8,bytes32,uint64)']).hex()
SELECTOR_DEPOSIT = "0x05e2ca17"


class Status(IntEnum):
    '''
    UNKNOWN:   "Deposit has no corresponding proposal"
    ACTIVE:    "Deposit is active for votes"
    PASSED:    "Deposit passed in voting"
    EXECUTED:  "Deposit was executed"
    CANCELLED: "Deposit was cancelled"
    '''
    UNKNOWN = 0,
    ACTIVE = 1,
    PASSED = 2,
    EXECUTED = 3,
    CANCELLED = 4,

    def __str__(self):
        return self.name


class DepositEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def DepositDecoder(_dict):
    deposit = ERC20Deposit()
    deposit.chain = _dict['chain']
    deposit.block = _dict['block']
    deposit.hash = _dict['hash']
    deposit.sender = _dict['sender']
    deposit.src = _dict['src']
    deposit.dst = _dict['dst']
    deposit.rId = _dict['rId']
    deposit.nonce = _dict['nonce']
    deposit.votes = _dict['votes']
    deposit.status = Status(_dict['status'])
    deposit.amount = _dict['amount']
    deposit.to = _dict['to']
    deposit.data_hash = _dict['data_hash']
    return deposit

class ERC20Deposit:
    def __init__(self):
        pass

    def toJSON(self):
        text = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return json.JSONDecoder().decode(text)

    @staticmethod
    def from_log(chain, tx, log):
        deposit = ERC20Deposit()
        deposit.chain = chain.name
        deposit.block = tx["blockNumber"]
        deposit.hash = log.transactionHash.hex()
        deposit.sender = tx["from"]
        deposit._decode_input(tx["input"])
        deposit._encode_data_hash(chain.handler2)
        deposit.src = chain.id
        deposit.dst = int(log.topics[1].hex(), 0)
        deposit.rId = log.topics[2].hex()
        deposit.nonce = int(log.topics[3].hex(), 0)
        deposit.votes = []
        deposit.status = Status.UNKNOWN
        return deposit
    
    @staticmethod
    def from_dict(_dict):
        deposit = ERC20Deposit()
        deposit.chain = _dict['chain']
        deposit.block = _dict['block']
        deposit.hash = _dict['hash']
        deposit.sender = _dict['sender']
        deposit.to = _dict['to']
        deposit.amount = _dict['amount']
        deposit.data_hash = _dict['data_hash']
        deposit.src = _dict['src']
        deposit.dst = _dict['dst']
        deposit.rId = _dict['rId']
        deposit.nonce = _dict['nonce']
        deposit.votes = _dict['votes']
        deposit.status = Status(_dict['status'])
        return deposit

    def update(self, bridge):
        proposal = get_proposal_safe(bridge, self.src, self.nonce, self.data_hash)
        self.votes = proposal[2]
        self.status = Status(proposal[4])

    def format(self):
        symbol = get_symbol(self.rId)
        decimal = get_decimal(self.rId)
        amount = self.amount / 10**decimal
        return f"{self.chain}: block= {self.block} tx= {self.hash} data_hash= {self.data_hash} from= {self.sender} to= {self.to} src= {self.src} dst= {self.dst} nonce= {self.nonce} votes= {len(self.votes)} status= {self.status} token= {symbol} amount= {amount}"

    def _decode_input(self, input):
        '''
            Example:
            MethodID: 0x05e2ca17
            [0]:  0000000000000000000000000000000000000000000000000000000000000000
            [1]:  000000000000000000000000000000c76ebe4a02bbc34786d860b355f5000301 ==> resourceID
            [2]:  0000000000000000000000000000000000000000000000000000000000000060
            [3]:  0000000000000000000000000000000000000000000000000000000000000054
            [4]:  000000000000000000000000000000000000000000000052c2a6938b42763000 ==> amount
            [5]:  0000000000000000000000000000000000000000000000000000000000000014
            [6]:  4fbf0609212b678862bee61dd025c257a42e6b3e000000000000000000000000 ==> recipient
        '''
        if input[:10] != SELECTOR_DEPOSIT:
            print("{}selector mismatch!{}".format(FAIL, ENDC))
            exit(-1)
        input = input[10:]
        params = []
        for index in range(0, len(input), 64):
            params.append(input[index: index + 64])
        self.to = f"0x{params[6][:40]}"
        self.amount = int(params[4], 16)

    def _encode_data_hash(self, handler):
        '''
            Example:
            0x
            000000000000000000000000000000000000000000000062b7739bedb2540000 ==> amount
            0000000000000000000000000000000000000000000000000000000000000014 ==> recipient address length (in bytes), 20
            a29cf8252323a1f3c2c19c14e48a194c023b35de                         ==> recipient address
        '''
        amount_hex = hex(self.amount)[2:].rjust(64, '0')
        data = f'0x{amount_hex}0000000000000000000000000000000000000000000000000000000000000014{self.to[2:]}'
        self.data_hash = web3.Web3.solidityKeccak(['address', 'bytes'], [handler, data]).hex()
