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
	env = os.environ.copy()
	branch = ['-b', 'master']
	dev = os.environ.get('BLE_DEV_NODE')
	if(os.environ.has_key("BLE_DEV_NODE")):
		branch = ['-b', 'dev']

	print branch

	if(len(sys.argv) > 1 and sys.argv[1] != ""):
		p = subprocess.call(['git', 'clone', '--depth=1', '--single-branch'] + branch + [sys.argv[1]], env=env)
	else:
		p = subprocess.call(['git', 'clone', '--depth=1', '--single-branch'] + branch + ['https://github.com/socifi/ble-positioning-node'], env=env)
	os.chdir(os.listdir('.')[0])
	p = subprocess.call(['pip', 'install', '--upgrade', '.'])


if __name__ == "__main__":
	main()
