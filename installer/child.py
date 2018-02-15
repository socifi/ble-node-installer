#!/usr/bin/python -u

from time import sleep
import subprocess
import tempfile
import os
import sys

def main():
	dirpath = tempfile.mkdtemp()
	os.chdir(dirpath)
	p = None
	branch = ['-b', 'master']
	if(os.environ.has_key("BLE_DEV_NODE")):
		branch = ['-b', os.environ['BLE_DEV_NODE']]

	if(len(sys.argv) > 1 and sys.argv[1] != ""):
		p = subprocess.call(['git', 'clone', '--depth=1', '--single-branch'] + branch + [sys.argv[1]])
	else:
		p = subprocess.call(['git', 'clone', '--depth=1', '--single-branch'] + branch + ['https://github.com/socifi/ble-positioning-node'])
	os.chdir(os.listdir('.')[0])
	p = subprocess.call(['pip', 'install', '--upgrade', '.'])


if __name__ == "__main__":
	main()
