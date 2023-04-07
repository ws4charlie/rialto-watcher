#!/usr/bin/env python3

import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger("BRIDGE")
