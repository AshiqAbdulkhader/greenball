from flask import Flask, render_template, Response
import serial
import sys
#ser=serial.Serial('COM8', 9600)
import cv2
import numpy as np
app = Flask(__name__)
cap=cv2.VideoCapture(0)

# @app.route('/')
# def index():
#     return render_template('index.html')

while(True):
    ret,frame=cap.read()
    cv2.imshow('frame',frame)
    output=frame.copy()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_green = np.array([65,60,60])
    upper_green = np.array([80,255,255])
    mask1=cv2.inRange(hsv,lower_green,upper_green)
    lower_green= (29, 86, 6)
    upper_green = (64, 255, 255)
    mask2=cv2.inRange(hsv,lower_green,upper_green)
    mask=mask1+mask2
    res=cv2.bitwise_and(frame,frame,mask=mask)
    gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    cv2.imshow('res',res)
    h,w,_=frame.shape
    tarea=h*w
    edged = cv2.Canny(gray, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 0:
            #ser.write(1)
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2)
            carea=cv2.contourArea(c)
            percent=carea*100/tarea
            position = 'Center'
            if x < (w/2):
                if y < (h/2):
                    position = 'Top Left'
                elif y > (h/2):
                    position = 'Bottom Left'
            elif x > (w/2):
                if y < (h/2):
                    position = 'Top Right'
                elif y > (h/2):
                    position = 'Bottom Right'

            if percent>1:
                sys.stdout.write(str(percent) + '\n' + position + '\n')
                # print(percent)

            else:
                sys.stdout.write('0' + '\n')
                #ser.write(0)
                # print(0)


    cv2.imshow('output',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
