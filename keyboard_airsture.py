import cv2
import numpy as np
import wx


app = wx.App(False)
(sx,sy) = wx.GetDisplaySize()
cam = cv2.VideoCapture(0)
(camx,camy)= (1024,7685)
cam.set(16,camx)
cam.set(9,camy)

'''cx=10
cy=20
x = 50
y =65
Tx=30
Ty=45'''

font = cv2.FONT_HERSHEY_SIMPLEX


def Print_key_1_0():
    cx=5
    x=50
    key=["`","1","2","3","4","5","6","7","8","9","0","<"]
    key2=["@","","","","5","6","7","8","9","0","<"]
    global font
    Tx=32
    for i in range(12):
        cv2.rectangle(frame,(cx,20),(x,65),(255,0,0),1)
        cv2.putText(frame, key[i],(Tx,39),font,0.7,(255,0,0),1,cv2.LINE_AA)
        Tx+=50
        cx+=50
        x+=50

def Print_key_Q_P():
    key=["Q","W","E","R","T","Y","U","I","O","P"]
    global font
    Tx=62
    cx=55
    x=100
    for i in range(10):
        cv2.rectangle(frame,(cx,70),(x,115),(255,0,0),1)
        cv2.putText(frame, key[i],(Tx,92),font,0.7,(255,0,0),1,cv2.LINE_AA)
        Tx+=50
        cx+=50
        x+=50

def Print_key_A_L():
    key=["A","S","D","F","G","H","H","K","L"]
    global font
    Tx=82
    cx=75
    x=120
    for i in range(9):
        cv2.rectangle(frame,(cx,120),(x,165),(255,0,0),1)
        cv2.putText(frame, key[i],(Tx,145),font,0.7,(255,0,0),1,cv2.LINE_AA)
        cx+=50
        x+=50
        Tx+=50

def Print_key_Z_M():
    key=["Z","X","C","V","B","N","M","Sft"]
    global font
    Tx=110
    cx=105
    x=150
    for i in range(8):
        cv2.rectangle(frame,(cx,170),(x,215),(255,0,0),1)
        cv2.putText(frame, key[i],(Tx,195),font,0.7,(255,0,0),1,cv2.LINE_AA)
        Tx+=50
        cx+=50
        x+=50
def Print_key_space():
    global font
    Tx=200
    cx=135
    x=330
    cv2.rectangle(frame,(cx,220),(x,265),(255,0,0),1)
    cv2.putText(frame, "Space",(Tx,245),font,0.7,(255,0,0),1,cv2.LINE_AA)
    
    
def Print_key_enter():
    global font
    Tx=340
    cx=335
    x=470
    cv2.rectangle(frame,(cx,220),(x,265),(255,0,0),1)
    cv2.putText(frame, "Enter",(Tx,245),font,0.7,(255,0,0),1,cv2.LINE_AA)
    
def clicker():
    
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


while(True):
    ret, frame = cam.read()
    Print_key_1_0()
    Print_key_Q_P()
    Print_key_A_L()
    Print_key_Z_M()
    Print_key_space()
    Print_key_enter()
    clicker()
    

    

    

    cv2.imshow('img',frame)
    if cv2.waitKey(5) == 27:
        break
