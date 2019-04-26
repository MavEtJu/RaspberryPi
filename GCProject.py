import time
import RPi.GPIO as gpio
from GCKeyboard import GCKeyboard
from GCSounds import GCSounds

# Keyboard

gpio.setmode(gpio.BCM)
keyboard = GCKeyboard(gpio)
sounds = GCSounds()

process = "global"

DIALSTATE_ONHOOK = 0
DIALSTATE_DIALTONE = 1
DIALSTATE_NUMBERCOLLECTING = 2
DIALSTATE_CALLING = 3
DIALSTATE_CONNECTED = 4
DIALSTATE_NEED_ONHOOK = 5

GAMESTATE_MAKING_CALL = 0
GAMESTATE_CALLTO_000 = 1
GAMESTATE_CALLTO_911 = 2
GAMESTATE_CALLTO_PIZZERIA = 3
GAMESTATE_CALLTO_MAVETJU = 4
GAMESTATE_CALLTO_RANDOM_ENCOUNTER = 4

CALLSTATE_000_SHOWOPTIONS = 0
CALLSTATE_000_GETOPTION = 1
CALLSTATE_000_AMBULANCE = 2
CALLSTATE_000_FIREBRIGADE = 3
CALLSTATE_000_POLICE = 4

dialState = DIALSTATE_ONHOOK
gameState = GAMESTATE_MAKING_CALL
callState000 = CALLSTATE_000_SHOWOPTIONS

counter = 0
number = ""

while 1:
	print
	print "dialState:%d counter:%d" % (dialState, counter),
	a = keyboard.getkeys()

	# Waiting for the handset to be lifted
	if a[0] == 0:
		dialState = DIALSTATE_ONHOOK
		counter = 0
		time.sleep(0.1)
		continue

	# Timeout after 30 seconds of waiting for the number
	if dialState == DIALSTATE_NEED_ONHOOK:
		time.sleep(0.1)
		continue;

	# Handset lifted, generate dialtone if needed and reset dialing info
	if a[0] == 1:
		if dialState == DIALSTATE_ONHOOK:
			dialState = DIALSTATE_DIALTONE
			counter = 0
			number = ""
			sounds.dialtone(1)
			continue

	if gameState == GAMESTATE_MAKING_CALL:

		# Keep track how long we have been waiting for the keys to be pressed
		# or a full number
		if dialState == DIALSTATE_DIALTONE or dialState == DIALSTATE_NUMBERCOLLECTING:
			counter += 1

		print "keys:",
		for p in range(0, len(a)):
			print a[p],

		key = keyboard.decode()
		if key is not None:
			print key,

		if key is not None and keyboard.changed():
			if dialState == DIALSTATE_DIALTONE:
				dialState = DIALSTATE_NUMBERCOLLECTING
				sounds.dialtone(0)
			sounds.dtmf(key)
			number += key
			if key == "*" or key == "#":
				dialState = DIALSTATE_NEED_ONHOOK
				sounds.error()
				continue

		if dialState == DIALSTATE_NUMBERCOLLECTING:
			if number == "0011":
				dialState = DIALSTATE_NEED_ONHOOK
				sounds.noOverseasCalls()
				continue

			if number == "000":
				dialState = DIALSTATE_CALLING
				gameState = GAMESTATE_CALLTO_000
				callState000 = CALLSTATE_000_SHOWOPTIONS
				sounds.ringing()
				continue

			if number == "911":
				dialState = DIALSTATE_CALLING
				gameState = GAMESTATE_CALLTO_911
				sounds.ringing()
				continue

			if number == "0430150894":
				dialState = DIALSTATE_CALLING
				gameState = GAMESTATE_CALLTO_MAVETJU
				sounds.ringing()
				continue

			if len(number) == 8 and number[0:1] != "0":
				dialState = DIALSTATE_CALLING
				gameState = GAMESTATE_CALLTO_RANDOM_ENCOUNTER
				continue;

		print number,

		time.sleep(3.0 / 100.0)

		if counter == 600:
			dialState = DIALSTATE_NEED_ONHOOK
			if dialState == DIALSTATE_DIALTONE:
				sounds.error()
			if dialState == DIALSTATE_NUMBERCOLLECTING:
				sounds.incompleteNumber()
			continue			

		continue

	if gameState == GAMESTATE_CALLTO_000:
		print "callState000:%d" % callState000,

		if sounds.playing():
			print "Still playing"
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_SHOWOPTIONS:
			sounds.play("000-options")
			callState000 = CALLSTATE_000_GETOPTION
			continue

		if callState000 == CALLSTATE_000_GETOPTION:
			key = keyboard.decode()
			if key is None:
				continue
			if key == "1":
				callState000 = CALLSTATE_000_AMBULANCE
				continue
			if key == "2":
				callState000 = CALLSTATE_000_FIREBRIGADE
				continue
			if key == "3":
				callState000 = CALLSTATE_000_POLICE
				continue
			sounds.play("000-options")
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_AMBULANCE:
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_FIREBRIGADE:
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE:
			time.sleep(0.1)
			continue

		print "Unknown callState000:%d" % callState000
		exit(0)

	print "Unknown gamestate:%d" % gameState
	exit(0)
