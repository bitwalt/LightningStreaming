from typing import List
from video_util.video_file import VideoFile
from pathlib import Path 
from swarm import SwarmGenerator
from lightning.invoice import Invoice

from logging import getLogger

logger = getLogger(__name__)

class VideoManager:
    """ A video manager for the LightningStreaming server. """

    def __init__(self, media_folder):
        """ Initialize the VideoManager with a list of VideoFiles. """
        self.media_folder = media_folder
        logger.debug("VideoManager > media_folder: {}".format(media_folder))
        self.video_files = self.get_video_files(Path(media_folder))
        
    def get_paths(self):
        return list(Path(self.media_folder).glob("*.mp4")) 
    
    def get_video_files(self, media_folder: Path) -> List[VideoFile]:
        video_files = {}
        for file_name in media_folder.glob("*.mp4"):
            v = VideoFile(file_name)
            video_files[file_name.stem] = v
        logger.debug(f"VideoManager : {video_files=}")
        return video_files
        
    def get_all_videos(self) -> List[VideoFile]:
        """ Return all VideoFiles in the list. """
        return list(self.video_files.values())
        
    def get_total_videos(self):
        return len(self.video_files)    
    
    def get_video_by_name(self, video_name) -> VideoFile:
        """ Return a VideoFile by name. """
        return self.video_files.get(video_name)
    
    def get_video_names(self) -> List[str]:
        return list(self.video_files.keys())
        
        
    def __str__(self) -> str:
        return f"VideoManager: \n{self.get_paths()}"
    
if __name__ == "__main__":
    video_manager = VideoManager("media/")
    print(video_manager.get_video_names())
    video_file = video_manager.get_video_by_name("mandelbrot_01")
    video_file.get_poster()
    invoice = Invoice("test", "lnd123abc...", 10)
    swarm = SwarmGenerator(video_file, invoice).generate()