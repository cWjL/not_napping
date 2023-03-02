#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import math
import time
import random
import string
import argparse
import webbrowser
import threading
import logging
import datetime
from multiprocessing import Queue, Process
from tkinter import *
from platform import uname

# if not os.path.isdir('{}/logs/'.format(os.getcwd())):
# 	os.mkdir('{}/logs/'.format(os.getcwd()))

# logger = logging.getLogger(__name__)
# logging.basicConfig(
# 					level=logging.DEBUG,
# 					format='%(asctime)s %(levelname)-8s %(message)s',
# 					datefmt='%a, %d %b %Y %H:%M:%S',
# 					filename='{}/logs/nap-{}.log'.format(
# 							os.getcwd(),
# 							datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 							),
# 					filemode='w'
# 					)

# logging.basicConfig(
# 	level=logging.DEBUG,
# 	filename='{}/logs/nap.log'.format(os.getcwd()),
# 	filemode='w'
# 	)
# log = logging.getLogger()
# multiprocessing_logging.install_mp_handler(log)

if 'linux' in uname().system.lower() or 'darwin' in uname().system.lower():
	if 'microsoft' in uname().release.lower():
		print("[X] ERROR: This script cannot be run from within WSL")
		sys.exit(0)
	else:
		import pyautogui
elif 'windows' in uname().system.lower():
	import pyautogui
	os.system("color")

WINDOW_POS = Queue()

def main():
	''' TODO main stuff '''
	parser = argparse.ArgumentParser()
	reqd = parser.add_argument_group('required arguments')
	reqd.add_argument(
		'-d',
		'--max-delay',
		action='store',
		dest='max',
		help='Max seconds to delay movement',
		required=True
		)
	parser.add_argument(
		'-m',
		'--mouse',
		action='store_true',
		dest='mouse',
		help='Move the mouse around at random interval'
		)
	parser.add_argument(
		'-t',
		'--type',
		action='store_true',
		dest='type',
		help='Type random garbage at random interval'
		)
	args = parser.parse_args()

	prefixes = []
	prefixes.append(f"[{FontColors.CGRN}*{FontColors.CEND}] ")
	prefixes.append(f"[{FontColors.CRED}!{FontColors.CEND}] ")
	prefixes.append(f"[{FontColors.CYLW}*{FontColors.CEND}] ")

	try:
		if args.max is not None:
			print(f"{prefixes[0]}Enter <CTRL+c> to exit")
			if args.mouse and not args.type:
				_move_mouse(prefixes, args)
			elif args.type and not args.mouse:
				_type_garbage(prefixes, args)
		else:
			print(f"{prefixes[1]}No interval provided")
	except KeyboardInterrupt:
		print(f"{prefixes[2]}Exiting...")

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
	print(f"{prefixes[0]}Starting mouse action.")
	print(f"{prefixes[0]}I will make {str(int(_MAX_ROTATION/360))} mouse rotations, delaying {str(_MAX)} seconds max.")

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

def _type_garbage(prefixes, args):
	'''
	Type random stuff in a note pad
	'''
	# _file_name_prefix = "file://"
	# _file_name = "not_napping.txt"
	# # if 'linux' in uname().system.lower() or 'darwin' in uname().system.lower():
	# # 	_file_name += "//"

	# # Set up file
	# with open(_file_name, "w") as scratch_pad:
	# 	scratch_pad.write("placeholder")

	# webbrowser.open("{}{}".format(_file_name_prefix, os.path.abspath(_file_name)))
	# Logging issue: can't write to single log from multiple processes.
	# See this: https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes

	
	# _queue = multiprocessing.Queue(-1)
	# listener = multiprocessing.Process(target=_listener_process,
	# 	args=(_queue, _listener_configurer))

	_MAX = int(args.max)
	_letters = string.ascii_lowercase

	print(f"{prefixes[0]}Starting typing action.")
	print(f"{prefixes[0]}I will create a window and type garbage into it, delaying {str(args.max)} seconds max.")

	print("1")
	_window_worker = M_Window()
	#_rt = _window_worker.show_window()
	_window_worker.show_window()
	sys.exit(0)
	print("2")
	_window_worker_p = Process(target=_window_worker.show_window())
	print("3")
	_window_worker_p.start()
	print("4")
	x_pos = WINDOW_POS.get()
	print("5")
	y_pos = WINDOW_POS.get()
	print("6")
	print("X:{}".format(str(x_pos)))
	print("7")
	print("Y:{}".format(str(y_pos)))
	print("8")

	try:
		print("9")
		#logger.info("Window position: X-{}, Y-{}".format(str(x_pos), str(y_pos)))
		while True:
			# Get random delay from 0 to --interval
			_random_delay = random.randint(0,_MAX)
			pyautogui.click(x_pos, y_pos)
			_char_arr = [random.choice(_letters) for i in range(_random_delay)]
			for _char in _char_arr:
				pyautogui.write(_char)
				time.sleep(1)

			pyautogui.write(" ")
			time.sleep(_random_delay)
	except:
		print("Bye")

	#_window_worker_p.join()

# multiprocessing log stuff
# From:
#	https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
# def _listener_configurer():
# 	root = logging.getLogger()
# 	h = logging.handlers.RotatingFileHandler('mptest.log', 'a', 300, 10)
# 	f = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# 	h.setFormatter(f)
# 	root.addHandler(h)

# def _listener_process(queue, configurer):
# 	configurer()
# 	while True:
# 		try:
# 			record = queue.get()
# 			if record is None:  # We send this as a sentinel to tell the listener to quit.
# 				break
# 			logger = logging.getLogger(record.name)
# 			logger.handle(record)  # No level or filter logic applied - just do it!
# 		except Exception:
# 			import sys, traceback
# 			print('Whoops! Problem:', file=sys.stderr)
# 			traceback.print_exc(file=sys.stderr)

class M_Window(object):

	def __init__(self):
		'''
		Create UI window and show it
		'''
		self.x_coord = 0
		self.y_coord = 0

	def show_window(self):
		'''
		Create a window for text to be entered in

		:param none
		:return none
		'''
		root = Tk()
		root.geometry("350x250")
		root.title("Robot Notes")
		root.minsize(height=250, width=350)
		root.maxsize(height=250, width=350)

		scrollbar = Scrollbar(root)
		scrollbar.pack(side=RIGHT,fill=Y)

		text_info = Text(root,yscrollcommand=scrollbar.set)
		text_info.pack(fill=BOTH)

		scrollbar.config(command=text_info.yview)

		WINDOW_POS.put(root.winfo_y())
		WINDOW_POS.put(root.winfo_x())
		# print(WINDOW_POS.empty())

		root.mainloop()
		print("after mainloop")

class FontColors:
	'''
	Terminal colors
	'''
	def __init__(self):
		self.CCYN = '\033[96m'
		self.CRED = '\033[31m'
		self.CGRN = '\033[92m'
		self.CYLW = '\033[93m'
		self.CBLU = '\033[94m'
		self.CPRP = '\033[95m'
		self.CEND = '\033[0m'
		self.CFON = '\33[5m'

if __name__ == "__main__":
	main()
	sys.exit(0)