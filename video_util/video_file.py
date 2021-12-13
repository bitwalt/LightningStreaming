from pathlib import Path
import os, sys
import cv2
import os
from time import sleep

""" RAM Requirements:

890 MB for chunks of 10 seconds (1080p video at 15 fps)
"""
MAX_CHUNK_SIZE = 9999999
PRICE = 1000

class VideoFile:
    """ A video file for the LightningStreaming peer server. """

    def __init__(self, url_path, seconds_chunk=1):
        self.url_path = url_path
        self.file_name = Path(url_path).stem
        self.opened = False
        self.price = PRICE
        self.video = self.open_video(url_path)
        
    def get_frame_chunk_len(self):
        return int(1 * self.fps) 
    
    def get_n_chunks(self):
        """Return tot number of video chunks (1 MB)"""
        return self.file_size // self.chunk_size + 1
    
    def get_price(self):
        return self.price
        
    def get_file_size(self):
        if os.path.isfile(self.url_path):
            return os.path.getsize(self.url_path)
        else:
            return 0
    
    def get_file_name(self):
        return self.file_name
    
    def get_url_path(self):
        return self.url_path
        
    def open_video(self, url_path):
        assert os.path.exists(self.url_path), f"{url_path} does not exist"

        video = cv2.VideoCapture(str(self.url_path))
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(video.get(cv2.CAP_PROP_FPS))
        self.n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))   
        self.frame_chunk_len = self.get_frame_chunk_len()
        self.file_size = self.get_file_size()
        self.opened = True
        return video
        
         
    def frame_iter(self):
        frame_num = 0
        while self.video.grab():
            chunk = []
            frame_num += 1
            frame = self.video.retrieve()[1]
            chunk.append(frame)
            if len(chunk) == self.frame_chunk_len:
                yield (frame_num, chunk)
                            
    def __repr__(self):
        return f"Video: {self.file_name} ({self.file_size} bytes)"    
    