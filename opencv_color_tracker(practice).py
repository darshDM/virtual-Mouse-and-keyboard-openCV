import cv2
import numpy as np
import pynput
from pynput.mouse import Controller,Button
import wx


app = wx.App(False)
(sx,sy) = wx.GetDisplaySize()
(camx,camy) = (320,240)
Mouse=Controller()

device = cv2. VideoCapture(0)
device.set(3,camx)
device.set(4,camy)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
while True:
        ret, frame = device.read()
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        
        lower_b = np.array([78,158,124])
        upper_b = np.array([138,255,255])
        lower_y = np.array([30,60,100])
        upper_y = np.array([50,255,255])
        

        mask = cv2.inRange(hsv, lower_b, upper_b)
        maskOpenB = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskCloseB = cv2.morphologyEx(maskOpenB,cv2.MORPH_CLOSE,kernelClose)
        maskFinalB = maskCloseB
        _,contsB,_ = cv2.findContours(maskFinalB.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        maskY = cv2.inRange(hsv, lower_y, upper_y)
        maskOpenY = cv2.morphologyEx(maskY,cv2.MORPH_OPEN,kernelOpen)
        maskCloseY = cv2.morphologyEx(maskOpenY,cv2.MORPH_CLOSE,kernelClose)
        maskFinalY = maskCloseY
        _,contsY,_ = cv2.findContours(maskFinalY.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if(len(contsB)>2000):
                print("Change the color... We trace blue colors more than one times")
                exit()

        else :
                for cnt in contsB:
                        M = cv2.moments(cnt)
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        frame = cv2.drawContours(frame, [box], 0, (0,255,0), 2)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        Mouse.position=(sx-(cx*sx/camx), cy*sy/camy)
                        
                for cnt in contsY:
                        M = cv2.moments(cnt)
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        frame = cv2.drawContours(frame, [box], 0, (0,255,0), 2)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])

                        if(len(contsY)>0):
                                Mouse.click(Button.left, 1)
                

                
        
                 
        cv2.imshow('mask',mask)
        #cv2.imshow('Result',result)
        cv2.imshow('image',frame)
        cv2.imshow('mask2',maskY)
        

        

        if cv2.waitKey(1) == 27:
            break

device.release()
cv2.destroyALLWindows()
