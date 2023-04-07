#!/usr/bin/env python3

import json
from jsonrpcserver import method, Result, Success, Error, serve
from rialto.bridges import CHAINS, get_chain, is_ERC20
from rialto.deposit import TOPIC_DEPOSIT, ERC20Deposit, DepositEncoder
import os.path as path
import sys
sdkpath = path.abspath(path.join(path.dirname(__file__), ".."))
sys.path.append(sdkpath)
from sdk import *

_rpc_url = "localhost"
_rpc_port = 8010


@method
def getPendingDeposits(bridge: str, incoming: bool):
    """get all pending deposits on the bridge"""
    if bridge.upper() not in CHAINS['Mainnet']:
        return Error(code=1, message="Bridge name must be one of (ETH, BSC, PLY, FTM)")

    # choose direction
    chain_src, chain_dst = get_chain(bridge, True)
    chain = chain_dst if incoming else chain_src

    # read pending deposits
    try:
        f_pending = chain.file_pending('r', create=False)
        if f_pending:
            return Success(json.load(f_pending))
        else:
            return Success("{}")
    except:
        return Error(code=2, message="Invalid json file")
    finally:
        if f_pending:
            f_pending.close()


@method
def getCancelledDeposits(bridge: str, incoming: bool):
    """get all cancelled deposits on the bridge"""
    if bridge.upper() not in CHAINS['Mainnet']:
        return Error(code=1, message="Bridge name must be one of (ETH, BSC, PLY, FTM)")

    # choose direction
    chain_src, chain_dst = get_chain(bridge, True)
    chain = chain_dst if incoming else chain_src

    # read cancelled deposits
    try:
        f_cancelled = chain.file_cancelled('r', create=False)
        if f_cancelled:
            return Success(json.load(f_cancelled))
        else:
            return Success("{}")
    except:
        return Error(code=2, message="Invalid json file")
    finally:
        if f_cancelled:
            f_cancelled.close()


@method
def queryDeposit(bridge: str, hash: str, incoming: bool):
    """query deposit by tx hash and bridge name"""
    if bridge.upper() not in CHAINS['Mainnet']:
        return Error(code=1, message="Bridge name must be one of (ETH, BSC, PLY, FTM)")

    # choose direction
    chain_src, chain_dst = get_chain(bridge, True)
    chain = chain_dst if incoming else chain_src

    # get transaction
    tx = get_transaction(chain.url, hash)
    if tx is None:
        return Error(code=3, message="Transaction not found")
    height = tx["blockNumber"]
    index = tx["transactionIndex"]

    # query deposit
    logs = get_logs(chain.url, chain.bridge, height, height, [TOPIC_DEPOSIT])
    if logs is None:
        return Error(code=4, message="Failed to get logs")
    for log in logs:
        rId = log.topics[2].hex()
        if index == log["transactionIndex"]:
            if is_ERC20(rId):
                deposit = ERC20Deposit.from_log(chain, tx, log)
                deposit.update(chain.bridge_contract2())
                return Success(deposit.toJSON())
            else:
                return Error(code=3, message=f"Unknown resource: {rId}")

    return Error(code=3, message="Transaction log not found")

def start_rpc():
    print("Starting HTTP server ...")
    print(f"URL: {_rpc_url}:{_rpc_port}")

    # Threading HTTP-Server
    serve(_rpc_url, _rpc_port)
