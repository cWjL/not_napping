#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
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

def main():
	''' TODO main stuff '''
	parser = argparse.ArgumentParser()
    parser.add_argument(
    					'-m',
    					'--mouse',
    					action='store_true',
    					dest='mouse',
    					help='Move mouse around to pretend you\'re awake'
    					)
    parser.add_argument(
				    	'-i',
				    	'--interact',
				    	action='store_true',
				    	dest='interact',
				    	help='Launch in interactive mode'
				    	)
	args = parser.parse_args()
	prefixes = []
	prefixes.append()

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