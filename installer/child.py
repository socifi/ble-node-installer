#!/usr/bin/python -u

from time import sleep
import subprocess
import os
import sys

def main():
	p = None
	if(sys.argv[1] != ""):
		p = subprocess.call(['git', 'clone', '--depth=1', '--single-branch', '-b', 'master', sys.argv[1]])
	else:
		p = subprocess.call(['git', 'clone', '--depth=1', '--single-branch', '-b', 'master', 'https://github.com/socifi/ble-positioning-node'])
	os.chdir(os.listdir('.')[0])
	p = subprocess.call(['pip', 'install', '.'])


if __name__ == "__main__":
	main()
