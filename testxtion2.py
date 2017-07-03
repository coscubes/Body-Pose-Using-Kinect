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
print type(depth.map)

while True:
    a = np.zeros((640, 480), np.uint8)
    context.wait_any_update_all()
    depthMap = depth.map

    frame = np.fromstring(depth.get_raw_depth_map_8(), "uint8").reshape(480,640)
    bgrframe = np.fromstring(image.get_raw_image_map_bgr(), dtype=np.uint8).reshape(image.metadata.res[1],image.metadata.res[0],3)
    gray = cv2.cvtColor(bgrframe, cv2.COLOR_BGR2GRAY)   
    face = face_cascade.detectMultiScale(gray, 1.3, 5) 
    for (x, y, w, h) in face:
        cv2.rectangle(bgrframe, (x,y), (x+w,y+h),(255,0,0),2)
        midx, midy = x + w/2, y + h/2
        value = depthMap[midx, midy]
        for i in range(640):
            for j in range(480):
                if depthMap[i , j] in range(value - 100, value + 100):
                    a[i, j] = 255
                else:
                    a[i, j] = 0
    a = np.transpose(a)
    cv2.imshow('frame', frame)
    cv2.imshow('frame1', a)
    cv2.imshow('frame rgb', bgrframe)

    pixel = depthMap[depthMap.width / 2, depthMap.height / 2]
    #   print depthMap.size, a.shape
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
        
cv2.destroyAllWindows()
