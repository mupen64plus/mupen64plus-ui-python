#!/bin/sh
apt-get -y install build-essential debhelper pyqt4-dev-tools dh-python python python-qt4 pyqt4-dev-tools
rm -rf ../../debian/
cp -fr ../debian/ ../../
cd ../../
dpkg-buildpackage -rfakeroot -tc -b
rm -rf debian/
