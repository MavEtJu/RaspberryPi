import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.OUT)
p = gpio.PWM(23, 50)
p.start(70)
for x in range(1, 10):
	p.ChangeFrequency(400)
	time.sleep(0.4)
	p.ChangeFrequency(450)
	time.sleep(0.2)
	p.ChangeFrequency(400)
	time.sleep(0.4)
	p.ChangeFrequency(0)
	time.sleep(2)
p.stop()
gpio.cleanup()

