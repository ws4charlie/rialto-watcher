import os
import sys
import time
import json
import requests

from web3 import Web3, HTTPProvider
from .constants import *
from .config import *


def get_chainid(url):
    w3 = Web3(HTTPProvider(url))
    try:
        return w3.eth.chain_id
    except:
        print("{}w3.eth.chain_id failed.{}".format(WARNING, ENDC))
        return None


def get_height(url):
    w3 = Web3(HTTPProvider(url))
    try:
        return w3.eth.blockNumber
    except:
        print("{}w3.eth.blockNumber failed.{}".format(WARNING, ENDC))
        return None


def get_height_safe(url, rest=5.0):
    height = get_height(url)
    while height is None:
        time.sleep(rest)
        height = get_height(url)
    return height


def get_logs(url, address, block_from, block_to, topics):
    w3 = Web3(HTTPProvider(url))
    try:
        return w3.eth.get_logs({
            'address': address,
            'fromBlock': hex(block_from),
            'toBlock': hex(block_to),
            'topics': topics,
        })
    except Exception as e:
        print("{}w3.eth.get_logs failed.{}{}".format(WARNING, e, ENDC))
        return None


def get_logs_safe(url, address, block_from, block_to, topics, rest=5.0):
    logs = get_logs(url, address, block_from, block_to, topics)
    while logs is None:
        time.sleep(rest)
        logs = get_logs(url, address, block_from, block_to, topics)
    return logs


def get_transaction(url, hash):
    w3 = Web3(HTTPProvider(url))
    try:
        return w3.eth.get_transaction(hash)
    except:
        print("{}w3.eth.get_transaction failed.{}".format(WARNING, ENDC))
        return None


def get_transaction_safe(url, hash, rest=5.0):
    tx = get_transaction(url, hash)
    while tx is None:
        time.sleep(rest)
        tx = get_transaction(url, hash)
    return tx


def wait_until(url, call, predict, poll=1.0, delay=2.0):
    # keep calling until condition is met
    fail, met = False, False
    while (not fail) and (not met):
        resp = call(url)
        if resp is None:
            time.sleep(poll)
            continue

        # return if prediction fail
        fail, met = predict(resp)
        if fail:
            break
        time.sleep(poll)

    # delay a bit
    time.sleep(delay)
    return resp


def wait_until_height_begin(url, height, strict_mode=False):
    """
        Parameters:
            url (str): url of EVM
            height (int): wait until the beginning of this height
            strict_mode (boolean): wait for the exact height or fails otherwise.
        Returns:
            (int, boolean): returns current height and status(succeed or failed)
    """
    # wait until a specific block begin(not end or commit)
    height = height-1

    # polling and wait
    def until(cur):
        fail = False
        arrives = False
        if height < cur:
            if strict_mode:
                print("{}Height {} already passed, current height is {}{}".format(WARNING, height, cur, ENDC))
                fail, arrives = (True, True)
            else:
                print("{}Height {} already passed, current height is {}. It's okay{}".format(WARNING, height+1, cur, ENDC))
                fail, arrives = (False, True)
        else:
            fail, arrives = (False, height == cur)
        return fail, arrives

    return wait_until(url, get_height, until, 1.0, 2.0)


def wait_for(url, blocks):
    # wait for some blocks
    cur_height = get_height(url)
    wait_until_height_begin(cur_height+blocks)


def env_to_url(name):
    # convert environment name to an endpoint
    if name.lower() not in KNOWN_ENVS:
        print('{}unknown environment: {}{}'.format(FAIL, name.lower(), ENDC))
        print('Environments supported: local, mainnet, testnet, mock, qa01, qa02')
        exit(5)
    else:
        return KNOWN_ENVS[name]


def to_web3_url(url):
    return '{}:8545'.format(url)


def to_abci_url(url):
    return '{}:26657'.format(url)
