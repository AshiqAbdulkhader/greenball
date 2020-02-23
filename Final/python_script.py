from flask import Flask, render_template, Response,request       #import libraries
import serial
ser=serial.Serial('/dev/ttyACM0', 9600)                          #object for serial communication
import cv2
import numpy as np
import time

app = Flask(__name__)                                           #object for flask

@app.route('/')                                                 #main function for rendering the html template
def index(status=None,percent=0,position=None):                     
    return render_template('index.html',Status=status,Position=position,Percent=percent)

def get_frame():                                                #function to extract the frames
    cap=cv2.VideoCapture(0)                                     #capture frame
    while True:
        ret,frame = cap.read()
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)               #convert color space from RGB to HSV
        lower_green = np.array([65,60,60])                      #limits of hsv values of light green
        upper_green = np.array([80,255,255])
        mask1=cv2.inRange(hsv,lower_green,upper_green)          #return 1 if the pixel belong in the range else 0
        lower_green= (29, 86, 6)                                # limits pof hsv values of dark green
        upper_green = (64, 255, 255)
        mask2=cv2.inRange(hsv,lower_green,upper_green)          #return 1 if the pixel belong in the range else 0
        mask=mask1+mask2                                        # pixel wise adding of masks
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        res=cv2.bitwise_and(frame,frame,mask=mask)              # resultant is generated as the part of the original frame which falls in the white region in the mask        
        gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)               # convert color space fromRGB to HSV
        h,w,_=frame.shape                                       # extract dimensions of the frame
        tarea=h*w                                               # area=h*w
        edged = cv2.Canny(gray, 30, 200)                        # detecting edges in the image
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   #finding contours
        if len(contours) > 0:                                   #if any contours are found
            c = max(contours, key=cv2.contourArea)              # find the largest contour by areas
            ((x, y), radius) = cv2.minEnclosingCircle(c)        # find the circle with minimum area that enclose the contour
            if radius > 0:
                ser.write('H')                                  # sends 'H' to arduino through serial communication
                status='True'
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2) # draw circle around the contour
                carea=cv2.contourArea(c)                        # find area of contour
                percent=carea*100/tarea                         # percentage of area covered by contour
                if (0<=x<=320 and 0<=y<=240):                   #finding position of the ball by comparing coordinates of the centre of the circle
                    position='top left'
                elif (320<x<=640 and 0<=y<=240):
                    position='top right'
                elif (0<=x<=320 and 240<y<=480):
                    position='bottom left'
                else:
                    position='bottom right'
                print(status,position,percent)
        else:
            ser.write('L')                                      #sends 'L' to arduino through serial communication
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
