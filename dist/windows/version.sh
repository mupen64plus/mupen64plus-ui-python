#!/bin/sh
VERSION=`cat ../../src/m64py/core/defs.py | grep FRONTEND_VERSION | awk -F' = ' '{print $2}' | tr -d '"'`
sed "s/{VERSION}/$VERSION/g" m64py.iss.in > m64py.iss
