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
    cv2.imshow('frame', frame)
    cv2.imshow('frame1', bgrframe)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
        
cv2.destroyAllWindows()
