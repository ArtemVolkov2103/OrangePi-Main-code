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
RECTCOLOR = (0, 255, 0)
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
	if len(approx) == 3:
		shape = "triangle"
	elif len(approx) == 4:
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)
		if ar >= 0.95 and ar <= 1.05:
			shape = "square"
		else: "rectangle"
	else:
		shape = "circle"
	return shape

if __name__ == '__main__':
    def nothing(*arg):
        pass

    #cv2.namedWindow("Form Determinant")
    cap = video.create_capture(1) 

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    high_blue = numpy.array((234, 253, 255), numpy.uint8)
    low_blue = numpy.array((18, 90, 121), numpy.uint8)
    while(True):
        flag, img = cap.read()
        height, width = img.shape[:2]
        
        img_copy = img
        #resized = imutils.resize(img_copy, width=300)
        #ratio = cap.shape[0] / float(resized.shape[0])
        ratio = 1

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        thres = cv2.inRange(hsv, low_blue, high_blue)
        thres = cv2.GaussianBlur(thres, (5, 5), 0)
        cnts = cv2.findContours( 
                                 thres.copy(), 
                                 cv2.RETR_EXTERNAL, 
                                 cv2.CHAIN_APPROX_SIMPLE 
                                )                       
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            if cv2.contourArea(c) <= BLOBSIZE:
                continue
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")

            cv2.drawContours(img_copy, [c], -1, CONTCOLOR, CTHICK)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect) 
            box = np.int0(box)
            cv2.drawContours(img_copy,[box],0,(255,0,0),2)

            M = cv2.moments(c)
            cX = 0
            cY = 0

            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)

            shapename = shapeDetect(c)
            #shapename = hue + " " + shapename
            #if shapename == "rectangle" or shapename == "square":
            cv2.rectangle(img_copy, (cX, cY), (cX + 140, cY + 30), (255, 255, 255), 30)
            cv2.putText(img_copy, shapename, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.imshow("Image", img_copy)

        k = cv2.waitKey(1)
        if k == 27:
            break
cap.release()
cv2.destroyAllWindows()
        
