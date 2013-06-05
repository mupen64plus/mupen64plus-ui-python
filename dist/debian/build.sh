#!/bin/sh
apt-get -y install build-essential debhelper
cp -fr ../debian/ ../../
cd ../../
dpkg-buildpackage -rfakeroot
rm -rf build/ debian/
