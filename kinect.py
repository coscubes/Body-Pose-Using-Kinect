#!/usr/bin/env python
from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv2  
import numpy as np

def doloop():
    global depth, rgb
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

    midx, midy = 0, 0
    while True:
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()
        # Build a two panel color image
        mn = np.min(depth)
        mx = np.max(depth)
        output = np.uint8((depth - mn)*255/(mx - mn))
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        face = face_cascade.detectMultiScale(gray, 1.3, 5) 
        for (x, y, w, h) in face:
            midx, midy = x + w / 2, y + h / 2

        ret2,th2 = cv2.threshold(output,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # d3 = np.dstack((depth,depth,depth)).astype(np.uint8)
        # da = np.hstack((d3,rgb))
        
        # Simple Downsample
        # cv2.imshow('both',np.array(da[::2,::2,::-1]))

        cv2.imshow('frame', th2)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        
doloop()

"""
IPython usage:
 ipython
 [1]: run -i demo_freenect
 #<ctrl -c>  (to interrupt the loop)
 [2]: %timeit -n100 get_depth(), get_rgb() # profile the kinect capture

"""
