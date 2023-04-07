#!/usr/bin/env python3

import argparse
from rialto import *
from multiprocessing import Process

def watcher_process(chain_config, latest):
    watcher = RialtoWatcher(chain_config)
    watcher.load(latest).watch()

def watch(args):
    # get chain config by address
    chain_src, chain_dst = validate_args(args)

    # start JSONRPC server
    if args.server:
        p0 = Process(target=start_rpc)
        p0.start()

    # start watcher
    p1 = Process(target=watcher_process, args=(chain_src, args.latest))
    p2 = Process(target=watcher_process, args=(chain_dst, args.latest))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

def query(args):
    print("deposit query not implemented")


def cancel(args):
    print("deposit cancellation not supported")

def validate_args(args):
    # get chain config
    chain_src, chain_dst = get_chain(args.bridge, args.testnet)

    # override urls if specified
    if args.url:
        chain_src.url = args.url
        chain_dst.url2 = args.url
    if args.url2:
        chain_src.url2 =  args.url2
        chain_dst.url =  args.url2

    # validate
    return chain_src.validate(), chain_dst.validate()

if __name__ == "__main__":

    # Initialize Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='web3 rpc endpoint of Findora chain ( override urls if specified )')
    parser.add_argument('--url2', help='web3 rpc endpoint of Foreign chain ( override urls if specified )')
    subparsers = parser.add_subparsers(dest='subparsers', help='sub-command help')

    # Initialize watch parser
    parser_watch = subparsers.add_parser('watch', help='watch deposits on the bridge')
    parser_watch.add_argument('--bridge', choices=['BSC', 'ETH', 'PLY', 'FTM'], help='Which bridge to watch')
    parser_watch.add_argument('-l', '--latest', help="Watch from latest height flag", action='store_true')
    parser_watch.add_argument('-t', '--testnet', help="Watch testnet flag", action='store_true')
    parser_watch.add_argument('-s', '--server', help="Run http server flag", action='store_true')
    parser_watch.set_defaults(func=watch)

    # Initialize query parser
    parser_query = subparsers.add_parser('query', help='query status of a deposit')
    parser_query.add_argument('--hash', help='the deposit transaction hash')
    parser_query.set_defaults(func=query)

    # Initialize cancel parser
    parser_cancel = subparsers.add_parser('cancel', help='cancel an expired deposit')
    parser_cancel.add_argument('--hash', help='the deposit transaction hash')
    parser_cancel.set_defaults(func=cancel)

    # Execute Command
    args = parser.parse_args()
    args.func(args)