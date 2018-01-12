from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from codecs import open
import os
from shutil import copyfile
from os import path
import stat
import ConfigParser

here = path.abspath(path.dirname(__file__))

name = 'ble_node_installer'
log_proxy = 'ble-logging.socifi.com'
log_proxy_port = '9339'
cronfile = '/etc/cron.hourly/ble_node_update'
configfile = '/etc/ble_node_installer/config.json'
scannerconfigfile = '/etc/ble_positioning_node/config.conf'
initialconfig = '{"ip": "34.236.161.213", "port": 5005}'
bleurl = 'https://b.socifi.com/'

version = '0.1.1'

ble_pos = ['https://github.com/socifi/ble-positioning-node/tarball/master#egg=ble_positioning_node-%s' % version]
if(os.environ.has_key("BLE_DEV_NODE")):
	ble_pos = ['https://github.com/socifi/ble-positioning-node/tarball/dev#egg=ble_positioning_node-%s' % version]

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

# Set cron job to check for updates
def custom_command():
	with open(cronfile, 'w') as f:
		f.write('#!/bin/bash\n'+name)
	st = os.stat(cronfile)
	os.chmod(cronfile, st.st_mode | stat.S_IEXEC)

	directory = os.path.dirname(configfile)
	if not os.path.exists(directory):
		os.makedirs(directory)
	with open(configfile, 'w') as f:
		f.write(initialconfig)

	directory = os.path.dirname(scannerconfigfile)
	if not os.path.exists(directory):
		os.makedirs(directory)
	config = ConfigParser.ConfigParser()
	config.read('config.conf')

	etcconfig = ConfigParser.RawConfigParser()

	etcconfig.add_section('Communication')
	etcconfig.set('Communication', 'log_proxy', log_proxy)
	etcconfig.set('Communication', 'log_proxy_port', log_proxy_port)
	etcconfig.set('Communication', 'Registration', bleurl+'node/register')
	etcconfig.set('Communication', 'Configuration', bleurl+'node/configuration')
	etcconfig.add_section('User')

	try:
		etcconfig.set('User', 'User_Key', config.get('User', 'User_Key'))
		etcconfig.set('User', 'User_Id', config.get('User', 'User_Id'))
		etcconfig.set('User', 'Brand_Id', config.get('User', 'Brand_Id'))
		etcconfig.set('User', 'Group_Id', config.get('User', 'Group_Id'))
	except ConfigParser.NoOptionError:
		print "You have to specify User_Key, User_Id, Brand_Id and Group_Id to install"
		exit(1)

	if(config.has_option('User', 'Name')):
		etcconfig.set('User', 'Name', config.get('User', 'Name'))

	with open(scannerconfigfile, 'wb') as conffile:
		etcconfig.write(conffile)


class CustomInstallCommand(install):
	def run(self):
		install.run(self)
		custom_command()

class CustomDevelopCommand(develop):
	def run(self):
		develop.run(self)
		custom_command()

class CustomEggInfoCommand(egg_info):
	def run(self):
		egg_info.run(self)
		custom_command()

setup(
	name='Ble Node Install',
	version=version,
	description='',
	long_description=long_description,
	url='',
	author='Socifi LTd.',
	author_email='code@socifi.com',
	license='MIT',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
	],
	cmdclass={
		'install': CustomInstallCommand,
		'develop': CustomDevelopCommand,
		'egg_info': CustomEggInfoCommand,
	},
	keywords='ble bluetooth',
	packages=[name],
	install_requires=['ble_positioning_node'],
	dependency_links=ble_pos,
	package_dir={name: 'installer'},
	entry_points={'console_scripts': [
		name+' = installer.install:main',
		'ble_node_install = installer.child:main',
		],
	},
)
