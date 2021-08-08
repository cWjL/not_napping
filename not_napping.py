#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import math
import time
import random
import datetime
import argparse
from platform import uname

if 'linux' in uname().system.lower() or 'darwin' in uname().system.lower():
	if 'microsoft' in uname().release.lower():
		print("[X] ERROR: This script cannot be run from within WSL")
		sys.exit(0)
	else:
		import pyautogui
elif 'windows' in uname().system.lower():
	import pyautogui
	os.system("color")

def main():
	''' TODO main stuff '''
	parser = argparse.ArgumentParser()
	reqd = parser.add_argument_group('required arguments')
	reqd.add_argument(
		'-m',
		'--max-delay',
		action='store',
		dest='max',
		help='Max seconds to delay movement',
		required=True
		)
	args = parser.parse_args()
	prefixes = []
	prefixes.append("[{}*{}] ".format(FontColors.CGRN,FontColors.CEND))
	prefixes.append("[{}!{}] ".format(FontColors.CRED,FontColors.CEND))
	prefixes.append("[{}*{}] ".format(FontColors.CYLW,FontColors.CEND))

	try:
		if args.max is not None:
			print("{}I'm awake. Not napping!".format(prefixes[0]))
			_move_mouse(prefixes, args)
		else:
			print("{}No interval provided".format(prefixes[1]))
	except KeyboardInterrupt:
		print("{}Exiting...".format(prefixes[2]))

	return

def _move_mouse(prefixes, args):
	'''
	Move the mouse in circles until you tell me to stop

	:param prefixes: array of formatted prefixes
	:param: args: arguments
	'''
	_R = 20
	_MAX_ROTATION = 1080
	_MAX = int(args.max)
	print("{}Starting mouse action.".format(prefixes[0]))
	print("{}I will make {} mouse rotations, delaying {} seconds max."
		.format(prefixes[0], str(int(_MAX_ROTATION/360)),str(_MAX)))
	print("{}CTRL+c to exit".format(prefixes[0]))

	# Get screen size
	(x,y) = pyautogui.size()
	# Get screen center
	(X,Y) = pyautogui.position(x/2,y/2)
	# Move to center of screen
	pyautogui.moveTo(X+_R,Y)

	# Continue until killed by user
	while True:
		# Get random delay from 0 to --interval
		_random_delay = random.randint(0,_MAX)
		# Move mouse in 3 circles (360*3)
		for i in range(_MAX_ROTATION):
			# Angle determines rotation rate
			if i%45 == 0:
				pyautogui.moveTo(X+_R*math.cos(math.radians(i)),Y+_R*math.sin(math.radians(i)))
		# Pause for random time in seconds
		time.sleep(_random_delay)

class FontColors:
	'''
	Terminal colors
	'''
	def __init__(self):
		pass
	CCYN = '\033[96m'
	CRED = '\033[31m'
	CGRN = '\033[92m'
	CYLW = '\033[93m'
	CBLU = '\033[94m'
	CPRP = '\033[95m'
	CEND = '\033[0m'
	CFON = '\33[5m'

if __name__ == "__main__":
	main()
	sys.exit(0)