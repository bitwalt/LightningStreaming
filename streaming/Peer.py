import logging
import asyncio
import os
import socket
import argparse
import time
import sys

from PyPPSPP.PeerProtocolUDP import PeerProtocolUDP
from PyPPSPP.PeerProtocolTCP import PeerProtocolTCP
from PyPPSPP.TrackerClientProtocol import TrackerClientProtocol
from PyPPSPP.SimpleTracker import SimpleTracker
from PyPPSPP.Hive import Hive
from multiprocessing import Process


class StreamingPeer(Process):
    
    """
    A Streaming peer implementing PPSPP Protocol
    (Peer-to-Peer Streaming Peer Protocol)
    """
    
    def __init__(self, args):
        super().__init__()
        self.swarms = []
        self.hive = Hive()
        self.tracker = SimpleTracker()
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(False)
        self.max_retry = 5
        self.args = args
        self.host = "127.0.0.1"
        self.port = 5555
       
    def connect_to_tracker(self):
        for i in range(self.max_retry):
            try:
                tracker_listen = self.loop.create_connection(
                    lambda:
                        TrackerClientProtocol(self.tracker), self.tracker_ip, self.tracker_port)
                tracker_transport, traceker_server = self.loop.run_until_complete(tracker_listen)
                break
            except Exception as exp:
                logging.warn('Exception connecting to tracker: {}'.format(exp))
                time.sleep(1)
               
        if i == self.max_retry - 1:
            logging.error('Failed to connect to the tracker!')
            return
        # TODO - check if connected to the Tracekr!
        if traceker_server is None:
            logging.error('Failed to connect to the tracker!')
            raise Exception()
        
        return traceker_server
 
    def run(self):
        # Create hive for storing swarms    
        self.tracker.set_hive(self.hive)
        
        tracker_server = self.connect_to_tracker()
        # TODO - check if connected to the Tracekr!
        self.tracker.set_tracker_protocol(tracker_server)
        
        listen = self.loop.create_server(
            lambda:
                    PeerProtocolTCP(self.hive), 
                    host = self.host,
                    port = self.port)
        protocol = self.loop.run_until_complete(listen)
    
        # At this point we have a connection to the tracker and have a listening (TCP/UDP) socket
        sw = self.hive.create_swarm(protocol, self.args)
    
        # Register with the tracker
        self.tracker.register_in_tracker(self.args.swarmid, self.port)
        self.tracker.get_peers(self.args.swarmid)

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        self.gently_close(protocol)
        
        
    def gently_close(self, protocol):
        self.hive.close_all_swarms()
        protocol.close()
        self.tracker.unregister_from_tracker(self.args.swarmid)
        self.loop.close()
        logging.shutdown()



if __name__ == "__main__":

    # LOG TO FILE

    LOG_TO_FILE = False
    output_dir = "./outdir/"
    os.makedirs(output_dir, exist_ok=True)
    result_id = socket.gethostname()+'_'+str(int(time.time()))
    
    if LOG_TO_FILE:
        idstr = 'runlog_'+result_id+'.log'
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', filename=output_dir+idstr)
    else:
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

    logging.info ("PyPPSPP starting")

    # Set the default parameters
    defaults = {}
    defaults['trackerip'] = "127.0.0.1"
    defaults['filename'] = "/Users/walter/Development/Lightning/LightningStreaming/PyPPSPP/media/mandelbrot_01.mp4"
    defaults['swarmid'] = "eaaf87bc7e3337264b4651d1e4a5d3e26f797eb7"
    defaults['filesize'] = 8051828
    defaults['live'] = False
    defaults['live_src'] = False
    defaults['tcp'] = True
    defaults['discard_window'] = 1000
    defaults['alto'] = False
    defaults['skip'] = False
    defaults['buffsz'] = 500
    defaults['dlfwd'] = 0
    defaults['vod'] = False

    # Parse command line parameters
    parser = argparse.ArgumentParser(description="Python implementation of PPSPP protocol")
    parser.add_argument("--tracker", help="Tracker IP address", nargs='?', default=defaults['trackerip'])
    parser.add_argument("--filename", help="Filename of the shared file", nargs='?', default=defaults['filename'])
    parser.add_argument("--swarmid", help="Hash value of the swarm", nargs='?', default=defaults['swarmid'])
    parser.add_argument("--filesize", help="Size of the file", nargs='?', type=int, default=defaults['filesize'])
    
    parser.add_argument("--live", help="Is this a live stream", action='store_true', default=defaults['live'])
    parser.add_argument("--livesrc", help="Is this a live stream source", action='store_true', default=defaults['live_src'])
    
    parser.add_argument("--numpeers", help="Limit the number of peers", nargs=1, type=int)
    parser.add_argument("--identifier", help="Free text that will be added to the results file", nargs='?')
    parser.add_argument("--tcp", help="Use TCP between the peers", action='store_true', default=defaults['tcp'])
    parser.add_argument('--discardwnd', help="Live discard window size", nargs='?', default=defaults['discard_window'])
    parser.add_argument('--alto', help="Use ALTO server to rank peers", nargs='?', type=bool, default=defaults['alto'])
    parser.add_argument('--altocosttype', help='ALTO cost type', nargs='?')
    parser.add_argument('--altoserver', help='ALTO server IP', nargs='?')
    parser.add_argument('--workdir', help='Change the working direcotry', nargs='?')
    parser.add_argument('--skip', help='Allow skipping chunks when framer is stuck', action='store_true', default=defaults['skip'])
    parser.add_argument('--buffsz', help='Buffer size (chunks) in Content Consumer', nargs='?', type=int, default=defaults['buffsz'])
    # In VOD scenarios and when data is available, a client might want to request only some 
    # chunks in 'front' of its' playback position. This parameter sets moving window
    # size, where reference point is last chunk fed into the video framer. 0 - No limit
    parser.add_argument('--dlfwd', help='Number of chunks to request after last played', nargs='?', type=int, default=defaults['dlfwd'])
    # Indicate that this is VOD
    parser.add_argument('--vod', help='This is Video-On-Demand CLIENT', action='store_true', default=defaults['vod'])

    # Start the program
    args = parser.parse_args()

    args.result_id = result_id
    args.output_dir = output_dir
    if args.discardwnd == 'None':
        args.discardwnd = None
    
    #main(args)
    stream_peer = StreamingPeer(args)
    stream_peer.start()
