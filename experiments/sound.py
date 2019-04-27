

from GCSounds import GCSounds
import time

s = GCSounds()

s.dialtone()

while 1:
	print s.isplaying()
	time.sleep(0.1)
