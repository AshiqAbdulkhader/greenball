import serial
ser=serial.Serial('COM8', 9600)
import cv2
import numpy as np
cap=cv2.VideoCapture(0)
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
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 10)
    if circles is not None:
        circles=np.round(circles[0,:]).astype("int")
        ser.write(1)
        print(1)
        for (x,y,r) in circles:
            cv2.circle(output,(x,y),r,(0,255,0),4)
        cv2.imshow("output", output)
    else:
        ser.write(0)
        print(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
    
