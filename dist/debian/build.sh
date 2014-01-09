#!/bin/sh
apt-get -y install build-essential debhelper pyqt4-dev-tools
cp -fr ../debian/ ../../
cd ../../
dpkg-buildpackage -rfakeroot
rm -rf build/ debian/
