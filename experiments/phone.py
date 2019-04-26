import RPi.GPIO as gpio
import time as time

speaker = 23
delay = 5.0 / 10000.0

gpio.setmode(gpio.BCM)
gpio.setup(speaker, gpio.OUT)

for x in range(10000):
	gpio.output(speaker, gpio.HIGH)
	time.sleep(2 * delay)
	gpio.output(speaker, gpio.LOW)
	time.sleep(delay)

