import RPi.GPIO as gpio
import time as time

def decode(a):
	if (a[3] == 1 and a[7] == 1):
		return "- 1",
	if (a[2] == 1 and a[7] == 1):
		return "- 2",
	if (a[1] == 1 and a[7] == 1):
		return "- 3",

	if (a[3] == 1 and a[6] == 1):
		return "- 4",
	if (a[2] == 1 and a[6] == 1):
		return "- 5",
	if (a[1] == 1 and a[6] == 1):
		return "- 6",

	if (a[3] == 1 and a[5] == 1):
		return "- 7",
	if (a[2] == 1 and a[5] == 1):
		return "- 8",
	if (a[1] == 1 and a[5] == 1):
		return "- 9",

	if (a[3] == 1 and a[4] == 1):
		return "- *",
	if (a[2] == 1 and a[4] == 1):
		return "- 0",
	if (a[1] == 1 and a[4] == 1):
		return "- #",

	return ""

ports = [ 4, 17, 18, 22, 23, 24, 25, 27 ]
delay = 50.0 / 1000.0

gpio.setmode(gpio.BCM)
for p in ports:
	gpio.setup(p, gpio.IN)

a = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
for x in range(10000):
	print x,
	for p in range(0, len(ports)):
		a[p] = gpio.input(ports[p])
		print a[p],

	print decode(a),

	print
	time.sleep(1.0 / 100.0)
