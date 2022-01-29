
from juliaset import JuliaSet

class GeneratorBuilder:
    
    def __init__(self):
        pass
    
    def generate(self, width=1000, height=1000, sec=3, kind='julia'):
        """
        Build a new video with the given args
        """
        if kind == 'julia':
            julia_set = JuliaSet(width, height, sec) 
            return julia_set.create_video()
        elif kind == 'mandelbrot':
            raise Exception('Set not implemented')
        else:
            raise Exception('Unknown kind of video')

