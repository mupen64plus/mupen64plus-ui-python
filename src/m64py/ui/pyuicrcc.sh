#!/bin/sh
for x in *.ui; do pyuic4 ${x} > ${x/.ui/}_ui.py; done
for x in *.qrc; do pyrcc4 ${x} > ${x/.qrc/}_rc.py; done
