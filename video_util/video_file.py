from pathlib import Path
import os, sys
import re
import cv2
import os
import time
import numpy as np
import binascii
from video_util.merkle_tree import MerkleHashTree
from settings import *
from logging import getLogger

logger = getLogger(__name__)

class VideoFile:
    """ A video file for the LightningStreaming peer server. """

    def __init__(self, file_path, chunk_size=CHUNK_SIZE, chunk_price=CHUNK_PRICE):
        self.file_path = file_path
        self.file_name = Path(file_path).stem
        self.chunk_size = chunk_size
        self.chunk_price = chunk_price
        self.get_stat(file_path)
        self.chunks = []
        self.chunk_iter = self.chunks_iterator()
      
    def get_stat(self, video_path: Path): 
        video = self.get_video(video_path)
        self.merkle_root = self.get_merkle_tree_hash(video_path)
        self.file_size = self.get_file_size(video_path)
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(video.get(cv2.CAP_PROP_FPS))
        self.n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))   
        self.duration = self.get_duration(self.n_frames, self.fps)
        self.total_chunks = self.get_n_chunks()
    
    def get_poster(self):
        video = self.get_video(self.file_path)
        video.grab()
        poster = video.retrieve()[1]
        video.release()
        return poster
    
    def get_video_price(self) -> int:
        return int(self.chunk_price * self.get_n_chunks())
        
    def get_duration(self, n_frames: int, fps: int) -> float:
        return n_frames / fps
     
    def get_n_chunks(self) -> int:
        """Return tot number of video chunks"""
        return self.file_size // self.chunk_size + 1
       
    def get_merkle_tree_hash(self, path:str) -> str:
        """Calculate a hash of a given file"""
        print('Calculating Merkle Tree Hash of file {}'.format(path))
        t_start = time.time()
        mht = MerkleHashTree('sha1', self.chunk_size)
        hash = mht.get_file_hash(path)
        if hash is None:
            logger.error('Error calculating file hash!')
            raise Exception('Error calculating file hash!')

        hash_str = str(binascii.hexlify(hash))
        logger.debug('Given file hash is: {}. Calculated in {:.2f} s.'.format(
            hash_str, time.time() - t_start))
        return hash_str
          
    def get_file_size(self, video_path:str) -> float:
        if os.path.isfile(video_path):
            return os.path.getsize(video_path)
        else:
            return 0
        
    def get_video(self, video_path):
        assert os.path.exists(video_path), f"{video_path} does not exist"
        video = cv2.VideoCapture(str(video_path))
        return video
        
    def reset_stream(self):
        self.frame_num = 0
        print("Resetting stream...")
        self.video = self.get_video(self.file_path)
        
          
    def chunks_iterator(self):
        frame_num = 0
        while frame_num < self.n_frames:    
            self.video.grab()
            frame_num += 1
            frame = self.video.retrieve()[1]
            yield frame_num, frame
        self.reset_stream()                    
    
    def as_dict(self):
        return {
            "file_name":    self.file_name,
            "merkle_root":  self.merkle_root,
            "file_path":    str(self.file_path),
            "file_size":    self.file_size,
            "duration":     self.duration,
            "width":        self.width,
            "height":       self.height,
            "fps":          self.fps,
            "n_frames":     self.n_frames,
            "total_chunks": self.total_chunks,
            "chunk_size":   self.chunk_size,
            "chunk_price":  self.chunk_price
        }
                            
    def __repr__(self):
        return f"Video: {self.file_name} ({self.file_size} bytes)"    
    