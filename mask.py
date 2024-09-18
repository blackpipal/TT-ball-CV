import cv2
import numpy as np
import serial

s=serial.Serial('com3')
s.baudrate=9600
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
cam.set(cv2.CAP_PROP_XI_FRAMERATE,20)
cam.set(10,150)

while(True):
    ret,frame=cam.read()
    fcopy=frame.copy()
    if ret:
        #U:19, 255, 255] L:5, 107, 0]
        Uthresh=np.array([19, 255, 255])
        Lthresh=np.array([5, 107, 0])
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,Lthresh,Uthresh)
        cv2.imshow("mask",mask)
        contours,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame,contours,-1,(0,255,0),2)
        if(len(contours)!=0):
            (x,y),radius=cv2.minEnclosingCircle(contours[0])
            cv2.circle(fcopy,(int(x),int(y)),int(radius),(255,0,0),3)
            s.write(str(x).encode())
        cv2.imshow("fcopy",fcopy)
        cv2.imshow("frame",frame)
    else:
        print(False)
        break
    if cv2.waitKey(1) and 0xFF==ord("q"):
            break
    
    
cv2.destroyAllWindows()
cam.release()