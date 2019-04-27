import RPi.GPIO as gpio

class GCKeyboard:

	def __init__(self, gpio_):
		self.ports = [4, 17, 18, 22, 23, 24, 25, 27]
		self.gpio = gpio_
		for port in self.ports:
			self.gpio.setup(port, gpio.IN)

		self.lastkeys = [0, 0, 0, 0, 0, 0, 0, 0]
		self.currentkeys = [0, 0, 0, 0, 0, 0, 0, 0]
		self.getkeys()
		return

	def decode(self, keys=None):
		if keys is None:
			keys = self.currentkeys

		retval = None
		if keys[7] == 1:
			if keys[3] == 1:
				retval = "1"
			if keys[2] == 1:
				retval = "2"
			if keys[1] == 1:
				retval = "3"

		if keys[6] == 1:
			if keys[3] == 1:
				retval = "4"
			if keys[2] == 1:
				retval = "5"
			if keys[1] == 1:
				retval = "6"

		if keys[5] == 1:
			if keys[3] == 1:
				retval = "7"
			if keys[2] == 1:
				retval = "8"
			if keys[1] == 1:
				retval = "9"

		if keys[4] == 1:
			if keys[3] == 1:
				retval = "*"
			if keys[2] == 1:
				retval = "0"
			if keys[1] == 1:
				retval = "#"

		return retval

	def changed(self):
		for idx in range(0, len(self.ports)):
			if self.lastkeys[idx] != self.currentkeys[idx]:
				return 1
		return 0

	def getkeys(self):
		for idx in range(0, len(self.ports)):
			self.lastkeys[idx] = self.currentkeys[idx]
			self.currentkeys[idx] = self.gpio.input(self.ports[idx])
		return self.currentkeys
