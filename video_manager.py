from typing import List
from video_util.video_file import VideoFile
from pathlib import Path 
from loguru import logger 

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
            print(v)
            video_files[file_name.stem] = v
            
        print(video_files)
        return video_files
        
    def get_total_videos(self):
        return len(self.video_files)    
    
    def get_all_videos(self) -> List[VideoFile]:
        """ Return all VideoFiles in the list. """
        return list(self.video_files.values())

    def get_video_by_name(self, video_name) -> VideoFile:
        """ Return a VideoFile by name. """
        return self.video_files.get(video_name)
    
    def get_video_names(self) -> List[str]:
        return list(self.video_files.keys())
        
        
    def __str__(self) -> str:
        return f"VideoManager: \n{self.get_paths()}"