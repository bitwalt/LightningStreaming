"""
A class to stream video from a file to a peer.
"""
from time import sleep
from threading import Thread
from video_util.video_file import VideoFile
import numpy as np
from queue import Queue

from logging import getLogger
logger = getLogger(__name__)

CHUNK_SEC = 1

class VideoStreamer(Thread):
    """
    A class to stream video from a file to a peer.
    """
    def __init__(self, video_file, node):
        """
        Initialize the Streamer.
        """
        Thread.__init__(self)
        self.video_file = video_file
        self.out_peer_node = node
        self.chunk_seconds = CHUNK_SEC
        self.running = True
        self.frames_iter = self.video_file.frame_itererator()
        self.frame_queue = Queue(maxsize=1)
 
        
    def show_video(self):
        for i, frame in enumerate(self.video_file.frame_itererator()):
            print(i, frame)
            

    def get_chunk_price(self):
        return self.video_file.get_price()
        
    def is_open(self):
        return self.video_file.opened


    def get_new_batch(self):
        """ Get a new batch of data. """ 
        if self.frames_iter is not None:    
            frame_index, frame = next(self.frames_iter, None)
        else: 
            raise Exception("No frames to stream")
        if frame is not None:
            frame = np.array(frame)
            
        message = {"cmd": "BATCH",
                    "index": frame_index,
                    "frame": frame
                }
        return message
    
    def get_video(self, file_name):
        pass
    
    def start_streaming(self, file_name):
        """ Start streaming the video. """
        self.file_name = file_name
        self.start()
        logger.debug("Streaming video...")
        sleep(5)
        return True
        
