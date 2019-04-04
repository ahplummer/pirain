##################################################

#           P26 ----> Relay_Ch1
#			P20 ----> Relay_Ch2
#			P21 ----> Relay_Ch3

##################################################
#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)

print("Setup The Relay Module is [success]")

try:

	GPIO.output(Relay_Ch1,GPIO.HIGH)
	print("Channel 1: Sending HIGH signal to contact to CLOSE the circuit...should allow sprinkler to function as normal!\n")

except:
	print("exception thrown")
	GPIO.cleanup()
