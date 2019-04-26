import RPi.GPIO as gpio
import time as time

class GCKeyboard:

	def __init__(self, gpio):
		self.ports = [ 4, 17, 18, 22, 23, 24, 25, 27 ]
		self.gpio = gpio;
		for p in self.ports:
			self.gpio.setup(p, gpio.IN)

		self.lastkeys = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
		self.currentkeys = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
		self.getkeys();
		return

	def decode(self, a = None):
		if a is None:
			a = self.currentkeys

		if a[3] == 1 and a[7] == 1:
			return "1"
		if a[2] == 1 and a[7] == 1:
			return "2"
		if a[1] == 1 and a[7] == 1:
			return "3"

		if a[3] == 1 and a[6] == 1:
			return "4"
		if a[2] == 1 and a[6] == 1:
			return "5"
		if a[1] == 1 and a[6] == 1:
			return "6"

		if a[3] == 1 and a[5] == 1:
			return "7"
		if a[2] == 1 and a[5] == 1:
			return "8"
		if a[1] == 1 and a[5] == 1:
			return "9"

		if a[3] == 1 and a[4] == 1:
			return "*"
		if a[2] == 1 and a[4] == 1:
			return "0"
		if a[1] == 1 and a[4] == 1:
			return "#"

		return None

	def changed(self):
		for p in range(0, len(self.ports)):
			if self.lastkeys[p] != self.currentkeys[p]:
				return 1
		return 0;

	def getkeys(self):
		for p in range(0, len(self.ports)):
			self.lastkeys[p] = self.currentkeys[p]
			self.currentkeys[p] = self.gpio.input(self.ports[p])
		return self.currentkeys

