#!/bin/sh
apt-get -y install build-essential debhelper pyqt5-dev-tools dh-python python python3-pyqt5 python3-pyqt5.qtopengl
rm -rf ../../debian/
cp -fr ../debian/ ../../
cd ../../
dpkg-buildpackage -rfakeroot -tc -b
rm -rf debian/
