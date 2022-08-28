# -*- coding: utf-8 -*-
# !usr/bin/env python3
# python3 /home/orangepi/Documents/python/pythonProject/main.py
# ctrl+c in command line to stop script

# deb [signed-by=/usr/share/keyrings/protonvpn-stable-archive-keyring.gpg] https://repo.protonvpn.com/debian stable main
# /dev/ttyUSB0
import os
import subprocess

import sys
import time

sys.path.append('/home/orangepi/Documents/python/pythonProject/venv/Lib/site-packages/')
import cv2
import video
import numpy

import glob
import serial
from timer import Timer

p = subprocess.Popen(['python3', 'blink_led.py'])

#s = serial.Serial('COM5', 9600) #для ноутбука
s = serial.Serial('/dev/ttyUSB0', 9600)
s.close()
s.open()

# цвет прямоугольника (B, G, R)
RECTCOLOR = (0, 255, 0)
# толщина линии прямоугольника
RTHICK = 2
# минимальный размер контуров пятна
BLOBSIZE = 1500

currentSec = 0.0
interval = 0.5
previousSec = 0.0
previousSec = 0.0

isObjectFound = False #флаг, найден ли объект
cameraAng = 90
camEdge = False
angle = 90
isRotated = False #повернул ли робот корпус к объекту
# определяем функцию проверки размера пятна
def checkSize(w, h):
    if (w * h) > BLOBSIZE:
        return True
    else:
        return False

if __name__ == '__main__':
    def nothing(*arg):
        pass


    cv2.namedWindow("out_window")
    cap = video.create_capture(1)
    #cap = video.create_capture(0) #для ноутбука

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    t = Timer()
    
    

    while True:
        
        flag, img = cap.read()
        # width = 640
        # height = 480

        height, width = img.shape[:2]
        edge = 100

        low_blue = numpy.array((90, 70, 70), numpy.uint8)
        high_blue = numpy.array((140, 255, 255), numpy.uint8)
        try:
			
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask_blue = cv2.inRange(img_hsv, low_blue, high_blue)

            result = cv2.bitwise_and(img_hsv, img_hsv, mask=mask_blue)
            result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

            moments = cv2.moments(mask_blue, 1)

            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']

            x = 0

            # побитово складываем оригинальную картинку и маску
            bitwise = cv2.bitwise_and(img, img, mask=mask_blue)
            # показываем картинку маски цвета
            # cv2.imshow("bitwise", bitwise)
            # удаляем цвет из маски
            gray = cv2.cvtColor(bitwise, cv2.COLOR_BGR2GRAY)
            # ищем контуры в картинке
            contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(contours) != 0:
                # выводим найденные контуры
                cv2.drawContours(img, contours, -1, 255, 4)
                # находим контуры бОльшего размера
                c = max(contours, key=cv2.contourArea)
                # получаем координаты прямоугольника, в который они вписаны
                x, y, w, h = cv2.boundingRect(c)
                # если прямоугольник достаточного размера...
                
                #if checkSize(w, h) and w > 80 and h > 80:
                    
                if not isObjectFound and w < 80 and h < 80:
                    isRotated = False
                    print("Search for object on " + str(cameraAng))
                    previousSec = time.perf_counter()
                    if cameraAng > 0 and not camEdge:
                        cameraAng = cameraAng - 1
                        s.write(bytes(str(cameraAng) + "," + str(60), 'utf-8'))
                        if cameraAng == 0:
                            camEdge = True
                    if cameraAng < 180 and camEdge:
                        cameraAng = cameraAng + 1
                        s.write(bytes(str(cameraAng) + "," + str(60), 'utf-8'))
                        if cameraAng == 180:
                            camEdge = False
                if dArea > 100 and w > 80 and h > 80:
                    if angle > 8:
                        cameraAng = cameraAng + 1
                        s.write(bytes(str(cameraAng) + "," + str(60), 'utf-8'))
                    if angle < -8:
                        cameraAng = cameraAng - 1
                        s.write(bytes(str(cameraAng) + "," + str(60), 'utf-8'))    
                    print("Обьект на " + str(cameraAng))
                    isObjectFound = True
                    if not isRotated:
                        if cameraAng > 90: # направо
                        	print("Right " + str(cameraAng))
                        	s.write(bytes(str(cameraAng) + "," + str(70), 'utf-8'))
                        	isRotated = True
                        else: # налево
                        	print("Left " + str(cameraAng))
                        	s.write(bytes(str(cameraAng) + "," + str(70), 'utf-8'))
                        	isRotated = True
                    cv2.rectangle(img, (x, y), (x + w, y + h), RECTCOLOR, RTHICK)
                    x = int(dM10 / dArea)
                    y = int(dM01 / dArea)
                    cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
                    distance = int(11033 / h) #дистанция, 230 пикселей = 48см
                    angle = int((320 - x) / 6.4)
                    #cv2.putText(img, "Width " + str(w), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.putText(img, "X " + str(x), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.putText(img, "angle " + str(angle), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(img, "distance " + str(distance), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    # nimers for not a non-stop sending symbols
                    if distance > 30 and distance < 50 and w < 230 and isObjectFound and isRotated:
                        #s.write(bytes(str(angle) + "," + str(distance), 'utf-8'))
                        cv2.rectangle(img, (310, 10), (340, 40), (255, 255, 255), 30)
                        cv2.putText(img, "F ", (315, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    isObjectFound = False
    
                '''if (x > (width / 2 + edge*2)) and x != 0:
                    cv2.rectangle(img, (0, 0), (30, height), (0, 255, 0), -1)
                        s.write(bytes("r", 'utf-8'))
                        cv2.putText(img, "R ", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                if (x < (width / 2 - edge*2)) and x != 0:
                    cv2.rectangle(img, (width - 30, 0), (width, height), (0, 255, 0), -1)
                        s.write(bytes("l", 'utf-8'))
                        cv2.putText(img, "L ", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                '''
            
            cv2.imshow("out_window", mask_blue)
            cv2.imshow("out_window", img)
        except:
            cap.release()
            raise

        ch = cv2.waitKey(50)
        # для выхода надо нажать esc
        if ch == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
p.terminate()   
s.close()


