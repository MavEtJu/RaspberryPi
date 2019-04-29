import random
import time
import RPi.GPIO as gpio
from GCKeyboard import GCKeyboard
from GCSounds import GCSounds

# Keyboard

gpio.setmode(gpio.BCM)
keyboard = GCKeyboard(gpio)
sounds = GCSounds()

random.seed()

DIALSTATE_ONHOOK = 0
DIALSTATE_DIALTONE = 1
DIALSTATE_NUMBERCOLLECTING = 2
DIALSTATE_CALLING = 3
DIALSTATE_CONNECTED = 4
DIALSTATE_NEED_ONHOOK = 5

GAMESTATE_MAKING_CALL = 0
GAMESTATE_CALLTO_000_REAL = 1
GAMESTATE_CALLTO_000_TOOEARLY = 2
GAMESTATE_CALLTO_911 = 3
GAMESTATE_CALLTO_PIZZERIA_REAL = 4
GAMESTATE_CALLTO_PIZZERIA_AGAIN = 5
GAMESTATE_CALLTO_RANDOM_ENCOUNTER = 6

CALLSTATE_000_SHOWOPTIONS = 0
CALLSTATE_000_GETOPTION = 1
CALLSTATE_000_AMBULANCE = 2
CALLSTATE_000_FIREBRIGADE = 3
CALLSTATE_000_POLICE = 4
CALLSTATE_000_POLICE_INTRO = 12
CALLSTATE_000_POLICE_DOYOUWANTDISCLAIMER = 9
CALLSTATE_000_POLICE_DOYOUWANTDISCLAIMER_RESPONSE = 10
CALLSTATE_000_POLICE_SHOWDISCLAIMER = 13
CALLSTATE_000_POLICE_ACCEPTDISCLAIMER = 5
CALLSTATE_000_POLICE_DISCLAIMERACCEPTED = 7
CALLSTATE_000_POLICE_CALLBACK_NOTUS = 5
CALLSTATE_000_POLICE_CALLBACK_US = 6
CALLSTATE_000_POLICE_FINISHED = 11

dialState = DIALSTATE_ONHOOK
gameState = GAMESTATE_MAKING_CALL
callState000 = CALLSTATE_000_SHOWOPTIONS
flagHasCalledPizzeria = False
flagNeedsToCall000 = False

counter = 0
number = ""

while 1:
	print
	print "dialState:%d counter:%d" % (dialState, counter),
	a = keyboard.getkeys()

	# Waiting for the handset to be lifted
	if a[0] == 0:
		if dialState != DIALSTATE_ONHOOK:
			if sounds.isPlaying():
				print
		sounds.stopPlaying()
		dialState = DIALSTATE_ONHOOK
		counter = 0
		time.sleep(0.1)
		continue

	# Timeout after 30 seconds of waiting for the number
	if dialState == DIALSTATE_NEED_ONHOOK:
		if sounds.isPlaying() is not True:
			sounds.reorder()
		time.sleep(0.1)
		continue

	# Handset lifted, generate dialtone if needed and reset dialing info
	if a[0] == 1:
		if dialState == DIALSTATE_ONHOOK:
			dialState = DIALSTATE_DIALTONE
			gameState = GAMESTATE_MAKING_CALL
			counter = 0
			number = ""
			sounds.dialtone()
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
				sounds.stopPlaying()
			sounds.dtmf(key)
			while sounds.isPlaying():
				time.sleep(0.1)
			number += key
			if key == "*" or key == "#":
				dialState = DIALSTATE_NEED_ONHOOK
				sounds.error()
				continue

		if dialState == DIALSTATE_NUMBERCOLLECTING:
			if number == "0011":
				dialState = DIALSTATE_NEED_ONHOOK
				sounds.error()
				continue

			if number == "000":
				dialState = DIALSTATE_CALLING
				if flagNeedsToCall000 is True:
					gameState = GAMESTATE_CALLTO_000_REAL
					callState000 = CALLSTATE_000_SHOWOPTIONS
				else:
					gameState = GAMESTATE_CALLTO_000_TOOEARLY
				sounds.ringing()
				continue

			if number == "888":
				dialState = DIALSTATE_CALLING
				if flagHasCalledPizzeria is False:
					gameState = GAMESTATE_CALLTO_PIZZERIA_REAL
					callState000 = CALLSTATE_000_SHOWOPTIONS
				else:
					gameState = GAMESTATE_CALLTO_PIZZERIA_AGAIN
				sounds.ringing()
				continue

			if number == "911":
				dialState = DIALSTATE_CALLING
				gameState = GAMESTATE_CALLTO_911
				sounds.ringing()
				continue

			if len(number) == 8 and number[0:1] != "0":
				dialState = DIALSTATE_CALLING
				gameState = GAMESTATE_CALLTO_RANDOM_ENCOUNTER
				continue

		print number,

		time.sleep(3.0 / 100.0)

		if counter == 600:
			dialState = DIALSTATE_NEED_ONHOOK
			if dialState == DIALSTATE_DIALTONE:
				sounds.error()
			if dialState == DIALSTATE_NUMBERCOLLECTING:
				sounds.error()
			continue

		continue

	if gameState == GAMESTATE_CALLTO_000_TOOEARLY:
		sounds.play("placeholder-000tooearly")
		dialState = DIALSTATE_NEED_ONHOOK
		continue

	if gameState == GAMESTATE_CALLTO_911:
		sounds.play("placeholder-911")
		dialState = DIALSTATE_NEED_ONHOOK
		continue

	if gameState == GAMESTATE_CALLTO_PIZZERIA_REAL:
		sounds.play("placeholder-pizzeriareal")
		flagHasCAlledPizzeria = True
		flagNeedsToCall000 = True
		dialState = DIALSTATE_NEED_ONHOOK
		continue

	if gameState == GAMESTATE_CALLTO_PIZZERIA_AGAIN:
		sounds.play("placeholder-pizzeria2ndtime")
		dialState = DIALSTATE_NEED_ONHOOK
		continue

	if gameState == GAMESTATE_CALLTO_RANDOM_ENCOUNTER:
		dialState = DIALSTATE_NEED_ONHOOK

		a = random.randint(0, 10)
		if a < 9:
			sounds.play("random-ringout")
			continue

		randoms = [
			"random-fax",
			"random-thenumberyouhavedialed",
			"random-areyoumymummy",
			"random-ELOtelephoneline",
			"random-OffTheWall",
			"random-R2D2",
			"random-BlondieHangingOnTheTelephone",
			"random-voicemail"
		]
		sounds.play(randoms[random.randint(0, len(randoms))])
		continue

	if gameState == GAMESTATE_CALLTO_000_REAL:
		print "callState000:%d" % callState000,

		if sounds.isPlaying():
			print "Still playing"
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_SHOWOPTIONS:
			sounds.play("placeholder-000real")
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
				callState000 = CALLSTATE_000_POLICE_INTRO
				continue
			sounds.play("000-options")
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_AMBULANCE:
			sounds.play("000-ambulance")
			dialState = DIALSTATE_NEED_ONHOOK
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_FIREBRIGADE:
			sounds.play("000-firebrigade")
			dialState = DIALSTATE_NEED_ONHOOK
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_INTRO:
			sounds.play("000-police-intro")
			callState000 = CALLSTATE_000_POLICE_DOYOUWANTDISCLAIMER
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_DOYOUWANTDISCLAIMER:
			sounds.play("000-police-doyouwantdisclaimer")
			callState000 = CALLSTATE_000_POLICE_DOYOUWANTDISCLAIMER_RESPONSE
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_DOYOUWANTDISCLAIMER_RESPONSE:
			key = keyboard.decode()
			if key is None:
				continue
			if key == "1":
				callState000 = CALLSTATE_000_POLICE_SHOWDISCLAIMER
				continue
			if key == "2":
				callState000 = CALLSTATE_000_POLICE_DISCLAIMERACCEPTED
				continue
			callState000 = CALLSTATE_000_POLICE_DOYOUWANTDISCLAIMER
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_SHOWDISCLAIMER:
			sounds.play("000-police-disclaimer")
			callState000 = CALLSTATE_000_POLICE_ACCEPTDISCLAIMER
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_ACCEPTDISCLAIMER:
			key = keyboard.decode()
			if key is None:
				continue
			if key == "1":
				callState000 = CALLSTATE_000_POLICE_DISCLAIMERACCEPTED
				continue
			if key == "2":
				callState000 = CALLSTATE_000_POLICE_DISCLAIMERACCEPTED
				continue
			callState000 = CALLSTATE_000_POLICE_SHOWDISCLAIMER
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_ACCEPTDISCLAIMER:
			sounds.play("000-police-afterdisclaimer")
			dialState = DIALSTATE_NEED_ONHOOK
			callState000 = CALLSTATE_000_POLICE_CALLBACK_NOTUS
			time.sleep(0.1)

		if callState000 == CALLSTATE_000_POLICE_CALLBACK_NOTUS:
			sounds.play("000-police-callback-others")
			dialState = DIALSTATE_NEED_ONHOOK
			callState000 = CALLSTATE_000_POLICE_CALLBACK_US
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_CALLBACK_US:
			sounds.play("000-police-callback-us")
			dialState = DIALSTATE_NEED_ONHOOK
			callState000 = CALLSTATE_000_POLICE_FINISHED
			time.sleep(0.1)
			continue

		if callState000 == CALLSTATE_000_POLICE_FINISHED:
			sounds.play("placeholder-000tooearly")
			time.sleep(0.1)
			continue

		print "Unknown callState000:%d" % callState000
		exit(0)

	print "Unknown gamestate:%d" % gameState
	exit(0)
