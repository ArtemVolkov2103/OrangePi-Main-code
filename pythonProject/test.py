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

sleep(1)
s.write(bytes(str(180) + "," + str(70), 'utf-8'))
while(1):
	'''if edge:
		for i in range(90, 180):
			s.write(bytes(str(i) + "," + str(60), 'utf-8'))
			print(i)
			sleep(0.1)
		edge = False'''
	if not edge:
		for i in range(180, 90):
			s.write(bytes(str(i) + "," + str(60), 'utf-8'))
			print(i)
			sleep(0.1)
		edge = True
