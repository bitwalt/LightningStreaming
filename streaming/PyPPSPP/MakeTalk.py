
import logging
import asyncio
import os
import socket
import argparse
import time
import sys

from PeerProtocolUDP import PeerProtocolUDP
from PeerProtocolTCP import PeerProtocolTCP
from TrackerClientProtocol import TrackerClientProtocol
from SimpleTracker import SimpleTracker
from Hive import Hive


# Create hive for storing swarms
hive = Hive()

# Start minimalistic event loop
loop = asyncio.get_event_loop()
loop.set_debug(False)

listen = loop.create_server(lambda: PeerProtocolTCP(hive),
                            host = "127.0.0.1",
                            port=5001)
protocol = loop.run_until_complete(listen)

sw = hive.create_swarm(protocol, args)