import os
import signal
import subprocess
from threading import Thread, Semaphore

class GCSounds:

	def __init__(self):
		self.filename = None
		self.process = None
		self.processlock = Semaphore()

		return

	def playy(self):
		self.processlock.acquire()
		self.process = subprocess.Popen(["aplay", "sounds/" + self.filename + ".wav"])
		self.processlock.release()
		self.process.wait()
		self.processlock.acquire()
		self.process = None
		self.processlock.release()
		return

	def play(self, filename):
		self.filename = filename
		self.processlock.acquire()
		self.process = True
		self.processlock.release()
		T = Thread(target = self.playy, args=[self.process])
		T.start()
		return

	def isplaying(self):
		self.processlock.acquire()
		if self.process is None:
			self.processlock.release()
			return False
		if self.process is True:
			self.processlock.release()
			return True
		try:
			self.process.poll()
		except:
			self.processlock.release()
			return True
		rv = self.process.returncode
		self.processlock.release()
		return rv is None

	def stopplaying(self):
		self.processlock.acquire()
		if self.process is None:
			self.processlock.release()
			return
		try:
			os.kill(self.process.pid, signal.SIGINT)
		except:
			self.processlock.release()
			return
		self.processlock.release()
		return

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

	def dialtone(self):
		self.play("dialtone-30s")
		return

	def error(self):
		self.play("error-1s")
		return
