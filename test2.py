from openni import *
import cv2
import numpy as np

context = Context()
context.init()


depth = DepthGenerator()
depth.create(context)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30
context.start_generating_all()


image = ImageGenerator()
image.create(context)
image.set_resolution_preset(RES_VGA)
image.fps = 30
context.start_generating_all()

face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

while True:
    context.wait_any_update_all()
    frame = np.fromstring(depth.get_raw_depth_map_8(), "uint8").reshape(480,640)
    bgrframe = np.fromstring(image.get_raw_image_map_bgr(), dtype=np.uint8).reshape(image.metadata.res[1],image.metadata.res[0],3)
    faces=face_cascade.detectMultiScale(bgrframe,1.3,5)
    
    blur = cv2.GaussianBlur(frame,(5,5),0)
    ret3,th3 = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    mask=cv2.bitwise_not(th3)
    th4=cv2.bitwise_and(bgrframe,bgrframe,mask=mask)
    for (x,y,w,h) in faces:
    	cv2.rectangle(bgrframe,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('frame', frame)
    cv2.imshow('frame1', bgrframe)
    cv2.imshow('frame3',th4)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
        
cv2.destroyAllWindows()
