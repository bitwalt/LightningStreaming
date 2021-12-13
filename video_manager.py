from typing import List
from video_util.video_file import VideoFile
from pathlib import Path 

class VideoManager:
    """ A video manager for the LightningStreaming server. """

    def __init__(self, media_folder):
        """ Initialize the VideoManager with a list of VideoFiles. """
        self.media_folder = media_folder
        self.video_files = self.get_video_files(Path(media_folder))
        
    def get_video_files(self, media_folder: Path) -> List[VideoFile]:
        video_files = {}
        for video_path in media_folder.glob('*.mp4'):
            if video_path.is_file():
                file_name = video_path.stem
                video_files[file_name] = VideoFile(video_path)
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
        return f"VideoManager: \n{self.get_video_names()}"