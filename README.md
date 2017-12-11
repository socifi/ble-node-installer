# Ble node installer

This package is intended as main installation package for SOCIFI's ble positioning system.

It is intended for installation on raspberry pi and works on raspbian lite. You can download it from
[SOCIFI's mirror](https://s3-eu-west-1.amazonaws.com/ble-storage/public/images/raspbian_lite.zip).
For it's checksum refer to this [file](https://s3-eu-west-1.amazonaws.com/ble-storage/public/images/raspbian_lite.sha256sum.txt)

## Installation

To install our suite you'll need to download repository from github, change at least User\_key, User\_Id, Brand\_Id and Group\_Id in configuration file and then install package via pip.

Commands to issue this are as follows. Please note that you migh use vi or any other text editor instead of nano.

```
sudo apt-get install git
git clone https://github.com/socifi/ble-node-installer
cd ble-node-installer
nano config.conf
\# change values in config file
sudo pip install .
```

## Notice

By installing this software you permit SOCIFI access the device remotely on your request. This package contains a software which allows SOCIFI doing the remote support.
