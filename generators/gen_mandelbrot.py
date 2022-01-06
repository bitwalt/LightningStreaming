# Credit to https://pythonturtle.academy/zooming-1013-into-mandelbrot-set-animation-with-python-source-code/

from PIL import Image
import numpy as np
import colorsys
import math
import cv2
from tqdm import tqdm

px, py = -0.7746806106269039, -0.1374168856037867 # Tante Renate
R = 3 
max_iteration = 2500
w, h = 300, 300
mfactor = 0.1

def get_fractal(x, X, y, Y):
    delta = (X-x)/300
    re, im = np.mgrid[x:X:delta, y:Y:delta]
    c = (re + 1j*im).reshape(im.shape[0], -1).T
    z = np.zeros_like(c)
    escape = np.zeros_like(np.absolute(c))
    for i in range(100):
        z = z*z + c # mandelbrot eqn
        idx = (np.absolute(z) > 4) & (escape == 0)
        escape[idx]  = i     
    return escape    
    
def get_fractal_at(x, y, D):
    return get_fractal(x-D, x+D, y-D, y+D)

def gen_fractal_video(filename):
    video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"MJPG"), 10, (w,h))  
    x = -.75
    y = -.25
    D = .1
    for i in tqdm(range(1000)):
        
        image = get_fractal_at(x,y,D) 
        x += 0.001
        y -= 0.001
        D -= 0.001
        print(image.shape)    
        cv2.imshow('image', np.array(image))
        cv2.waitKey(10)
 
def Mandelbrot(x,y,max_iteration,minx,maxx,miny,maxy):
    zx = 0
    zy = 0
    RX1, RX2, RY1, RY2 = px-R/2, px+R/2,py-R/2,py+R/2
    cx = (x-minx)/(maxx-minx)*(RX2-RX1)+RX1
    cy = (y-miny)/(maxy-miny)*(RY2-RY1)+RY1
    i=0
    while zx**2 + zy**2 <= 4 and i < max_iteration:
        temp = zx**2 - zy**2
        zy = 2*zx*zy + cy
        zx = temp + cx
        i += 1
    return i

def gen_Mandelbrot_image(sequence):
  bitmap = Image.new("RGB", (w, h), "white")
  pix = bitmap.load()
  for x in range(w):
    for y in range(h):
      c=Mandelbrot(x,y,max_iteration,0,w-1,0,h-1)
      v = c**mfactor/max_iteration**mfactor
      hv = 0.67-v
      if hv<0: hv+=1
      r,g,b = colorsys.hsv_to_rgb(hv,1,1-(v-0.1)**2/0.9**2)
      r = min(255,round(r*255))
      g = min(255,round(g*255))
      b = min(255,round(b*255))
      pix[x,y] = int(r) + (int(g) << 8) + (int(b) << 16)
  return bitmap
        
def gen_Mandelbrot_video(filename):

    video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"MJPG"), 10, (w,h))  
    R=3
    f = 0.975
    RZF = 1/1000000000000
    k=1
    iters = 10
    for _ in tqdm(range(iters)):
        if R>RZF:
            mfactor = 0.5 + (1/1000000000000)**0.1/R**0.1
            print(k,mfactor)
            image = gen_Mandelbrot_image(k)
            R *= f
            k+=1    
            video.write(np.array(image))
            
if __name__ == '__main__':
    
    gen_Mandelbrot_video('Mandelbrot.avi')
    #gen_fractal_video("Mandelbrot_02.avi")
    