import os
import json

with open(os.path.join(os.path.dirname(__file__), 'Bridge.json')) as f:
    info_json = json.load(f)

BRIDGE_ABI = info_json["abi"]
