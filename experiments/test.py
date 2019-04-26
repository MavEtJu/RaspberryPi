import RPi.GPIO as gpio
import time as time

port = 17
delay = 50.0 / 1000.0

gpio.setmode(gpio.BCM)
gpio.setup(port + 0, gpio.OUT)

for x in range(10000):
	gpio.output(port + 0, gpio.HIGH)
	time.sleep(delay)
	gpio.output(port + 0, gpio.LOW)
	time.sleep(delay)
	print x 

