#!/usr/bin/python

import os, time
import stat
import subprocess
import socket
import io
import sys
import requests
import json
import tempfile
import struct
import bluetooth._bluetooth as bluez
from datetime import datetime

version = '0.1.0'
ip = '34.236.161.213'
port = 5005
configfile = '/etc/ble_node_installer/config.json'

def mac_get():
	devId = 0
	try:
		sock = bluez.hci_open_dev(devId)
	except:
		print 'bluetooth error'
		sys.exit(1)
	return read_local_bdaddr(sock)

def read_local_bdaddr(sock):
	flt = bluez.hci_filter_new()
	opcode = bluez.cmd_opcode_pack(bluez.OGF_INFO_PARAM, bluez.OCF_READ_BD_ADDR)
	bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
	bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
	bluez.hci_filter_set_opcode(flt, opcode)
	sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
	bluez.hci_send_cmd(sock, bluez.OGF_INFO_PARAM, bluez.OCF_READ_BD_ADDR )
	pkt = sock.recv(255)
	status,raw_bdaddr = struct.unpack("xxxxxxB6s", pkt)
	assert status == 0
	t = [ "%02X" % ord(b) for b in raw_bdaddr ]
	t.reverse()
	bdaddr = "".join(t)
	return bdaddr.lower()



def main():
	mac = mac_get()
	print mac
	# Load configuration
	config = json.load(open(configfile))
	# Try to communicate with server
	if('ip' in config):
		ip = config['ip']
	if('port' in config):
		port = config['port']
	# Check for updates
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	s.send('{"version":"'+version+'", "mac":"'+mac+'", "time": "'+str(datetime.now())+'" "config":'+json.dumps(config)+'}')
	data_json = s.recv(1024)
	s.close()
	print "received data:", data_json

	try:
		data = json.loads(data_json)
	except:
		
		exit(1)

	# Update config
	if('config' in data):
		print "writing config"
		config = data['config']
		try:
			json.dump(config, open(configfile, 'w'))
		except:
			pass

	# Update tracking package

	if('update' in data):
		print "updating package"
		link = ""
		if('link' in data['update']):
			link = data['update']['link']
		p = subprocess.Popen(['ble_node_install', link])


	# Download and run additional script (ie. for self update)
	if('script' in data):
		tmp = ""
		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(data['script']['commands'])
			tmp =  f.name
		st = os.stat(f.name)
		os.chmod(f.name, st.st_mode | stat.S_IEXEC)
		if(data['script']['type'] == 'bash'):
			p = subprocess.Popen(['bash', f.name])
		if(data['script']['type'] == 'python'):
			p = subprocess.Popen(['python', f.name])

if __name__ == "__main__":
	main()
