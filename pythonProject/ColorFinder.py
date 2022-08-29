import cv2 as cv
import numpy as np
import time
from time import sleep

def getColor(image):
    target = [int(image.shape[1] / 2), int(image.shape[0] / 2)]

    b, g, r = image[target[1], target[0]]
    image = cv.circle(image, (320, 240), 10, (int(b), int(g), int(r)), 2)
    cv.imshow('image', image)
    print(f'colour = {b}, {g}, {r}')
    sleep(0.1)

cap = cv.VideoCapture(1)
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #getColor(frame)
    # define range of blue color in HSV
    upper_blue = np.array([140, 195, 235])
    lower_blue = np.array([88, 70, 90])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    #cv.imshow('frame',frame)
    #cv.imshow('mask',mask)
    cv.imshow('res',res)
    
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
