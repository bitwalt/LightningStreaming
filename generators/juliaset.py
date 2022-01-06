import numpy as np
import matplotlib.pyplot as plt


def julia_set(c=-0.4 + 0.6j, height=1000, width=1000, x=0, y=0, zoom=1, max_iterations=100):
    # To make navigation easier we calculate these values
    x_width = 1.5
    y_height = 1.5*height/width
    x_from = x - x_width/zoom
    x_to = x + x_width/zoom
    y_from = y - y_height/zoom
    y_to = y + y_height/zoom

    # Here the actual algorithm starts
    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    z = x + 1j * y

    # Initialize z to all zero
    c = np.full(z.shape, c)

    # To keep track in which iteration the point diverged
    div_time = np.zeros(z.shape, dtype=int)
    # To keep track on which points did not converge so far
    m = np.full(c.shape, True, dtype=bool)

    for i in range(max_iterations):
        z[m] = z[m]**2 + c[m]

        m[np.abs(z) > 2] = False

        div_time[m] = i
    return div_time

import cv2
from tqdm import tqdm
from random import random

max_iterations = 100


def gen_video(width, height):
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    writer = cv2.VideoWriter('julia.mp4', fourcc, 10, (width, height))
    for i in tqdm(range(1, max_iterations)):
        c = -0.4 + 0.6j
        zoom = i        
        img = julia_set(c=c, height=200, width=200, x=0, y=0, zoom=zoom, max_iterations=200)
        img = img.astype(np.uint8)
        img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
        writer.write(img)
    
    writer.release()
    
gen_video(100, 100)