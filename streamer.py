"""
A class to stream video from a file to a peer.
"""
from time import sleep
from threading import Thread
from video_util.video_file import VideoFile

from loguru import logger

CHUNK_SEC = 1


class VideoStreamer(Thread):
    """
    A class to stream video from a file to a peer.
    """
    def __init__(self, video_file: VideoFile):
        """
        Initialize the Streamer.
        """
        Thread.__init__(self)
        self.video_file = video_file
        self.chunk_seconds = CHUNK_SEC
        self.running = True

    def get_chunk_price(self):
        return self.video_file.get_price()
        
    def is_open(self):
        return self.video_file.opened


    def get_new_batch(self):
        """ Get a new batch of data. """
        return "BATCH"
    
    def get_video(self, file_name):
        pass
    
    def start_streaming(self, file_name):
        """ Start streaming the video. """
        self.file_name = file_name
        self.start()
        logger.debug("Streaming video...")
        sleep(5)
        return True
        
    
    def run(self):
        self.running = True
        self.video_iterator = self.video.frame_iter()
        