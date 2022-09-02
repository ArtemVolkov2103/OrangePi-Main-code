import sys
sys.path.append('/home/orangepi/Documents/python/pythonProject/venv/Lib/site-packages/')

import cv2
import video
import numpy
import numpy as np
import imutils
import time
from time import sleep

# цвет прямоугольника (B, G, R)
RECTCOLOR = (0, 0, 255)
# толщина линии прямоугольника
RTHICK = 2
# минимальный размер контуров пятна
BLOBSIZE = 2000

CONTCOLOR = (0, 255, 0)

CTHICK = 2

FRAMESIZE = (640, 480)

def shapeDetect(c):
	shape = ""
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * peri, True)
	if len(approx) == 4 or len(approx) == 5:
		shape = "rectangle"

	return shape

if __name__ == '__main__':
    def nothing(*arg):
        pass

    cap = video.create_capture(1) 

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    high_blue = numpy.array((124, 255, 255), numpy.uint8)
    low_blue = numpy.array((70, 125, 75), numpy.uint8)
    while(True):
        flag, img = cap.read()
        
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        img_copy = cv2.filter2D(img, -1, sharpen_kernel)
        #img_copy = img
        hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

        thres = cv2.inRange(hsv, low_blue, high_blue)
        thres = cv2.medianBlur(thres, 13)
                
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
        closed = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)
        cnts = cv2.findContours( 
                                 closed.copy(), 
                                 cv2.RETR_CCOMP, 
                                 cv2.CHAIN_APPROX_SIMPLE 
                                )                       
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            if cv2.contourArea(c) <= BLOBSIZE:
                continue
            
            cv2.drawContours(img, [c], -1, CONTCOLOR, CTHICK)

            M = cv2.moments(c)
            cX = 0
            cY = 0

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

            shapename = shapeDetect(c)
            if shapename == "rectangle":
               cv2.rectangle(img, (cX, cY), (cX + 140, cY + 25), (255, 255, 255), 30)
               cv2.putText(img, shapename, (cX, cY + 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        #cv2.imshow("thres", closed)
        cv2.imshow("Image", img)

        k = cv2.waitKey(1)
        if k == 27:
            break
cap.release()
cv2.destroyAllWindows()
        
