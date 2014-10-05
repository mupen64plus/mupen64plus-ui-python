#!/bin/sh
yum install rpm-build PyQt5-devel -y
VERSION=`cat ../../src/m64py/core/defs.py | grep FRONTEND_VERSION | awk -F' = ' '{print $2}' | tr -d '"'`
sed "s/{VERSION}/$VERSION/g" m64py.spec.in > m64py.spec
cd ../../ && python setup.py sdist
mkdir -p ~/rpmbuild/SOURCES
cp dist/m64py-${VERSION}.tar.gz ~/rpmbuild/SOURCES/
rpmbuild -ba dist/redhat/m64py.spec
