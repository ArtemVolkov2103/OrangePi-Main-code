# -*- coding: utf-8 -*-
# !usr/bin/env python3
# python3 /home/orangepi/Documents/python/pythonProject/main.py
# ctrl+c in command line to stop script

# deb [signed-by=/usr/share/keyrings/protonvpn-stable-archive-keyring.gpg] https://repo.protonvpn.com/debian stable main
# /dev/ttyUSB0
from tkinter import *
import os
from os import system

import sys
import time

sys.path.append('/home/orangepi/Documents/python/pythonProject/venv/Lib/site-packages/')
import cv2
import video
import numpy

import glob
import serial
from timer import Timer
system("echo 228 | sudo tee /sys/class/gpio/export") # This will create the PH4 instance
system("echo out | sudo tee /sys/class/gpio/gpio228/direction") # This will set the PH4 as OUTPUT

flag = False

def on_closing():
        root.destroy()
        print ("Closed")
        system("echo 0 | sudo tee /sys/class/gpio/gpio228/value")
        system("echo 228 | sudo tee /sys/class/gpio/unexport")


def click_button():
    global clicks
    global flag 
    flag = not flag
    try:
       
       if flag:
           buttonText.set("ON")
           system("echo 1 | sudo tee /sys/class/gpio/gpio228/value") # This will set the PH4 HIGH
       else:
           buttonText.set("OFF")
           system("echo 0 | sudo tee /sys/class/gpio/gpio228/value") # This will set the PH4 LOW
    except KeyboardInterrupt:
       print ("KeyboardInterrupt")
       system("echo 0 | sudo tee /sys/class/gpio/gpio228/value")
       system("echo 228 | sudo tee /sys/class/gpio/unexport")


root = Tk()
root.title("Python Window")
root.geometry("200x100")
buttonText = StringVar()
buttonText.set("OFF")
btn = Button(textvariable=buttonText, command=click_button, background="#555", foreground="#ccc", padx="20", pady="8", font="16")
btn.pack() 
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

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


# определяем функцию проверки размера пятна
def checkSize(w, h):
    if (w * h) > BLOBSIZE:
        return True
    else:
        return False


oldSym = "f"

if __name__ == '__main__':
    def nothing(*arg):
        pass


    cv2.namedWindow("out_window")
    cap = video.create_capture(1)
    #cap = video.create_capture(0) #для ноутбука

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    t = Timer()
    t.start()
    currentSec = 0.0
    interval = 3.0
    previousSec = 0.0

    while True:
        
        currentSec = time.perf_counter()
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
                distance = int(11033 / h) #дистанция, 230 пикселей = 48см
                angle = int((320 - x) / 6.4)
                if checkSize(w, h) and w > 80:
                    # выводим его
                    cv2.rectangle(img, (x, y), (x + w, y + h), RECTCOLOR, RTHICK)
                    #cv2.putText(img, "Width " + str(w), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.putText(img, "Height " + str(h), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.putText(img, "angle " + str(angle), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(img, "distance " + str(distance), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                if dArea > 200 and w > 80:
                    x = int(dM10 / dArea)
                    y = int(dM01 / dArea)
                    cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
                    # nimers for not a non-stop sending symbols
                    if h > 230 and (x < (width / 2 + edge * 2)) and (x > (width / 2 - edge * 2)):
                        s.write(bytes(str(angle) + "," + str(distance), 'utf-8'))
                        cv2.putText(img, "F ", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

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
    
s.close()


