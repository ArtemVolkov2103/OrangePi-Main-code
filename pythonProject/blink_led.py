#!/usr/bin/env python
"""
sudo python3 blink_led.py
(position of letter in alphabet - 1) * 32 + pin number 
PH4 = (8 - 1) * 32 + 4 = 228
Basic blinking led example.
The led on A20-OLinuXino-MICRO  blinks with rate of 1Hz like "heartbeat".
"""
from tkinter import *
 

import os
import sys
from os import system

from time import sleep

system("echo 228 | sudo tee /sys/class/gpio/export") # This will create the GPIO6 instance
system("echo out | sudo tee /sys/class/gpio/gpio228/direction") # This will set the GPIO6 as OUTPUT
#system("echo 1 | sudo tee /sys/class/gpio/gpio228/value") # This will set the GPIO6 HIGH


flag = False

def on_closing():
        root.destroy()
        print ("Goodbye.")
        system("echo 0 | sudo tee /sys/class/gpio/gpio228/value")
        system("echo 228 | sudo tee /sys/class/gpio/unexport")


def click_button():
    global clicks
    global flag 
    flag = not flag
    try:
       print ("Press CTRL+C to exit")
       if flag:
           system("echo 1 | sudo tee /sys/class/gpio/gpio228/value") # This will set the GPIO6 HIGH
           #sleep(0.5)
       else:
           system("echo 0 | sudo tee /sys/class/gpio/gpio228/value") # This will set the GPIO6 HIGH
           #sleep(0.5)
    except KeyboardInterrupt:
       print ("Goodbye.")
       system("echo 0 | sudo tee /sys/class/gpio/gpio228/value")
       system("echo 228 | sudo tee /sys/class/gpio/unexport")


root = Tk()
root.title("Python Window")
root.geometry("400x300")
btn = Button(text="On/Off", command=click_button)
btn.pack() 
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

