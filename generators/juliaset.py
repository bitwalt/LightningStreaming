import re
import numpy as np
import matplotlib.pyplot as plt

import cv2
from tqdm import tqdm
from time import time
import os 
max_iterations = 100
MEDIA = '../media/'
FPS = 10

class JuliaSet:
    
    def __init__(self, width, height, sec=10, c=-0.4 + 0.6j ):
        self.width = width
        self.height = height
        self.sec = sec
        self.c = c
                
    def get_fractal(self, x=0, y=0, zoom=1, max_iterations=100):
        # To make navigation easier we calculate these values
        x_width = 1.5
        y_height = 1.5* self.height/ self.width
        x_from = x - x_width/zoom
        x_to = x + x_width/zoom
        y_from = y - y_height/zoom
        y_to = y + y_height/zoom
        # Here the actual algorithm starts
        x = np.linspace(x_from, x_to, self.width).reshape((1, self.width))
        y = np.linspace(y_from, y_to, self.height).reshape((self.height, 1))
        z = x + 1j * y
        # Initialize z to all zero
        c = np.full(z.shape, self.c)
        # To keep track in which iteration the point diverged
        image = np.zeros(z.shape, dtype=int)
        # To keep track on which points did not converge so far
        m = np.full(c.shape, True, dtype=bool)
        for i in range(max_iterations):
            z[m] = z[m]**2 + c[m]
            m[np.abs(z) > 2] = False
            image[m] = i
        return image.astype(np.uint8)

    def create_video(self):
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        filename = f'julia_{int(time())}.avi'
        print(f'Creating video {filename}')
        file_path = os.path.join(MEDIA, filename)
        writer = cv2.VideoWriter(file_path, fourcc, FPS, (self.width, self.height))
        tot_frames = FPS * self.sec + 1
        for i in tqdm(range(1, tot_frames)):
            zoom = i * 2
            x = 0.001 * i       
            y = 0.001 * i       
            img = self.get_fractal(x,y,zoom)
            img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
            writer.write(img)
        writer.release()
        print(f'Video saved to {file_path}')
        return file_path

    def show_video(self, video):
        while video.isOpened():
            ret, frame = video.read()
            if ret:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('Video ended')
                break
        video.release()
        cv2.destroyAllWindows()
        
    def get_video(self, file_path):
        video = cv2.VideoCapture(file_path)
        return video

if __name__ == '__main__':
    julia_set = JuliaSet(width=1000, height=1000, sec=5)
    file_path = julia_set.create_video()
    video = julia_set.get_video(file_path)
    julia_set.show_video(video)