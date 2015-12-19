#!/bin/sh
apt-get -y install build-essential debhelper dh-python python3 python3-pyqt5 pyqt5-dev-tools
rm -rf ../../debian/
cp -fr ../debian/ ../../
cd ../../
dpkg-buildpackage -rfakeroot -tc -b
rm -rf debian/
