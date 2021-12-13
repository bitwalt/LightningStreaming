import subprocess as sp
import shlex
from loguru import logger

OUT_VIDEO_FPS = 20

class VideoSaver:

    def __init__(self, output_path, height, width):
        self.output_path = output_path
        self.height = height
        self.width = width
        self.fps = OUT_VIDEO_FPS
        self.process = self.create_videowriter()

    def create_videowriter(self):
        process = sp.Popen(shlex.split(
                f'ffmpeg -y -s {self.width}x{self.height} \
                    -pixel_format bgr24 -f rawvideo -r {self.fps} \
                    -i pipe: -vcodec libx265 -pix_fmt yuv420p -crf 24 {self.output_path}')
                    , stdin=sp.PIPE)
        logger.debug("FFMPEG_VideoSaver created!")
        return process
        
    def write(self, frame):
        if self.process is not None:
            self.process.stdin.write(frame.tobytes())        
        
    def close(self):
        # Close and flush stdin
        if self.process is not None:
            self.process.stdin.close()
            # Wait for sub-process to finish
            self.process.wait()
            # Terminate the sub-process
            self.process.terminate()
            self.process = None