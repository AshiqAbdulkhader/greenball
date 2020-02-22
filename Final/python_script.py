from flask import Flask, render_template, Response,request
import serial
ser=serial.Serial('/dev/ttyACM0', 9600)
import cv2
import numpy as np
import time

app = Flask(__name__)

@app.route('/')
def index(status=None,percent=0,position=None):
    return render_template('index.html',Status=status,Position=position,Percent=percent)

def get_frame():
    cap=cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_green = np.array([65,60,60])
        upper_green = np.array([80,255,255])
        mask1=cv2.inRange(hsv,lower_green,upper_green)
        lower_green= (29, 86, 6)
        upper_green = (64, 255, 255)
        mask2=cv2.inRange(hsv,lower_green,upper_green)
        mask=mask1+mask2
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        res=cv2.bitwise_and(frame,frame,mask=mask)
        gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        h,w,_=frame.shape
        tarea=h*w
        edged = cv2.Canny(gray, 30, 200)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 0:
                ser.write('H')
                status='True'
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2)
                carea=cv2.contourArea(c)
                percent=carea*100/tarea
                if (0<=x<=320 and 0<=y<=240):
                    position='top left'
                elif (320<x<=640 and 0<=y<=240):
                    position='top right'
                elif (0<=x<=320 and 240<y<=480):
                    position='bottom left'
                else:
                    position='bottom right'
                print(status,position,percent)
        else:
            ser.write('L')
            status='False'
            print(status)
        imgencode=cv2.imencode('.jpg',frame)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

    del(cap)

@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
