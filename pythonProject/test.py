import os
import subprocess
import sys
import time
from time import sleep

sys.path.append('/home/orangepi/Documents/python/pythonProject/venv/Lib/site-packages/')
import cv2
import video
import numpy

import glob
import serial
from timer import Timer

p = subprocess.Popen(['python3', 'blink_led.py'])
sleep(1)
s = serial.Serial('/dev/ttyUSB0', 9600)
s.close()
s.open()

edge = True
a = 90

sleep(1)
s.write(bytes(str(180) + "," + str(70), 'utf-8'))
sleep(0.5)
while(1):
	if edge == True:
		for i in range(90, 180):
			a = a + 1
			s.write(bytes(str(a) + "," + str(60), 'utf-8'))
			print(a)
			sleep(0.5)
		edge = False
		
	if not edge:
		for i in range(90, 180):
			a = a - 1
			s.write(bytes(str(a) + "," + str(60), 'utf-8'))
			print(a)
			sleep(0.5)
		edge = True
