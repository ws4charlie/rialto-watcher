import time
from ..colors import *

def get_proposal(bridge, id, nonce, data_hash):
    try:
        return bridge.functions.getProposal(id, nonce, data_hash).call()
    except BaseException as e:
        print("{}getProposal failed. {} {}".format(WARNING, e, ENDC))
        return None

def get_proposal_safe(bridge, id, nonce, data_hash, rest=5.0):
    proposal = get_proposal(bridge, id, nonce, data_hash)
    while proposal is None:
        time.sleep(rest)
        proposal = get_proposal(bridge, id, nonce, data_hash)
    return proposal
