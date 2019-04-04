##################################################

#           P26 ----> Relay_Ch1
#			P20 ----> Relay_Ch2
#			P21 ----> Relay_Ch3

##################################################
# !/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1, GPIO.OUT)

print("Setup The Relay Module is [success]")

try:

    GPIO.output(Relay_Ch1, GPIO.LOW)
    print("Channel 1: Sending LOW signal to contact to OPEN the circuit...should override the sprinkler!\n")

except:
    print("exception thrown")
    GPIO.cleanup()
