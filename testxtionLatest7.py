from openni import *
import cv2
import numpy as np
import cmath as math

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
        
        
        print "It's Working"
        headx,heady=midx,midy
        neckx,necky=headx,y+7*h/4
        shoulderWidth=7*w/3
        shoulder1x,shoulder1y=neckx-shoulderWidth/2,necky
        shoulder2x,shoulder2y=neckx+shoulderWidth/2,necky
        bgrframe=cv2.circle(bgrframe,(shoulder1x,shoulder1y),5,(0,0,255),-1)
        
        bgrframe = cv2.line(bgrframe,(shoulder1x,shoulder1y),(shoulder2x,shoulder2y),(0,255,0),2)
        bgrframe = cv2.line(bgrframe,(headx,heady),(neckx,necky),(0,255,0),2)
        bgrframe=cv2.circle(bgrframe,(shoulder2x,shoulder2y),5,(0,0,255),-1)
        bgrframe=cv2.circle(bgrframe,(headx,heady),5,(0,0,255),-1)
        bgrframe=cv2.circle(bgrframe,(neckx,necky),5,(0,0,255),-1)
        upperArmLength=6*shoulderWidth/10
        lowerArmLength=6*shoulderWidth/9
        #for uppeArm and lowerArm
        for theta in range(0,360):
        	upper1x,upper1y=int(shoulder1x-upperArmLength*math.sin(-1*theta)),int(shoulder1y+upperArmLength*math.cos(-1*theta))
        	if upper1x<640 and upper1y<480 and upper1x>0 and upper1y>0 and upper1x<shoulder1x:
        		if depthMap[upper1x,upper1y] in range(value-100,value+100):
        			bgrframe=cv2.line(bgrframe,(shoulder1x,shoulder1y),(upper1x,upper1y),(0,255,0),2)
        			bgrframe=cv2.circle(bgrframe,(upper1x,upper1y),5,(0,0,255),-1)
        			#lowerArm
        			for theta in range(0,360):
        				lower1x,lower1y=int(upper1x+lowerArmLength*math.sin(-1*theta)),int(upper1y+lowerArmLength*math.cos(-1*theta))
        				if lower1x>0 and lower1x<640 and lower1y<480 and lower1y>0 and lower1x<upper1x:
        					if depthMap[lower1x,lower1y] in range(value-100,value+100):
        						bgrframe=cv2.line(bgrframe,(upper1x,upper1y),(lower1x,lower1y),(0,255,0),2)
        						cv2.circle(bgrframe,(lower1x,lower1y),5,(0,0,255),-1)
        						break
        			break
        #upperArm2 and lowerArm2
        for theta in range(0,360):
        	upper2x,upper2y=int(shoulder2x+upperArmLength*math.sin(-1*theta)),int(shoulder2y+upperArmLength*math.cos(-1*theta))		
        	if upper2x<640 and upper2y<480 and upper2x>0 and upper2y>0 and upper2x>shoulder2x:
        		if depthMap[upper2x,upper2y] in range(value-100,value+100):
        			bgrframe=cv2.line(bgrframe,(shoulder2x,shoulder2y),(upper2x,upper2y),(0,255,0),2)
        			cv2.circle(bgrframe,(upper2x,upper2y),5,(0,0,255),-1)
        			for theta in range(80,360):
        				lower2x,lower2y=int(upper2x+lowerArmLength*math.sin(theta)),int(upper2y+lowerArmLength*math.cos(theta))
        				if lower2x>0 and lower2y>0 and lower2x<640 and lower2y<480 and lower2x>upper2x:
        					if depthMap[lower2x,lower2y] in range(value-100,value+100):
        						bgrframe=cv2.line(bgrframe,(upper2x,upper2y),(lower2x,lower2y),(0,255,0),2)
        						cv2.circle(bgrframe,(lower2x,lower2y),5,(0,0,255),-1)
        						break
        			break
        print "It's working"
        print value
        if (midx+w)<640 and (midx-w)>0: ###correction2:cut the horizontal !(ROI)
		    for i in range(640):
		        for j in range(y,480): ###correction1;;Process from y to 480
		            if depthMap[i , j] in range(value - 100, value + 100):
		                a[i, j] = 255
		            else:
		                a[i, j] = 0
        else:
		    for i in range(640):
		        for j in range(y,480): ###correction1;;Process from y to 480
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
