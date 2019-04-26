import os
import signal
import subprocess
from threading import Thread

class GCSounds:

	def __init__(self):
		self.filename = None
		self.process = None
		self.inDialtone = 0
		return

	def playy(self):
		self.process = subprocess.Popen(["aplay", self.filename + ".wav"])
		print self.process.pid
		return

	def play(self, filename):
		self.filename = filename
		T = Thread(target = self.playy)
		T.start()
		return

	def playing(self):
		return self.process.poll() is None

	def dtmf(self, key):
		if key == "#":
			key = "hash"
		if key == "*":
			key = "star"
		self.play("dtmf-" + key)
		return

	def ringing(self):
		self.play("ringing-3.5s")
		return

	def dialtone(self, enable = 1):
		if enable == 0:
			if self.inDialtone == 1:
				os.kill(self.process.pid, signal.SIGINT)
				self.inDialtone = 0
		else:
			self.inDialtone = 1
			self.play("dialtone-30s")
		return
	
	def error(self):
		self.play("error-1s");
		return
