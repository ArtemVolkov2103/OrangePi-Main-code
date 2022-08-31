import cv2 as cv
import numpy as np
import time
from time import sleep

# цвет прямоугольника (B, G, R)
RECTCOLOR = (0, 255, 0)
# толщина линии прямоугольника
RTHICK = 2
# минимальный размер контуров пятна
BLOBSIZE = 1500

def shapeDetect(c):
	shape = ""
	peri = cv2.arcLength(c, Type)
	approx = cv2.approxPolyDP(c, 0.04 * peri, True)

if __name__ == '__main__':
    def nothing(*arg):
        pass

	cv2.namedWindow("out_window")
		cap = video.create_capture(1)
		#cap = video.create_capture(0) #для ноутбука

		cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		
		height, width = img.shape[:2]
        edge = 100

        #low_blue = numpy.array((90, 70, 70), numpy.uint8)
        #high_blue = numpy.array((140, 255, 255), numpy.uint8)
        high_blue = numpy.array((104, 255, 255), numpy.uint8)
        low_blue = numpy.array((82, 140, 88), numpy.uint8)
