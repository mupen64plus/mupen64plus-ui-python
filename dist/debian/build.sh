#!/bin/sh
apt-get -y install build-essential debhelper pyqt5-dev-tools dh-python python python-pyqt5 python-pyqt5.qtopengl
rm -rf ../../debian/
cp -fr ../debian/ ../../
cd ../../
dpkg-buildpackage -rfakeroot -tc -b
rm -rf debian/
