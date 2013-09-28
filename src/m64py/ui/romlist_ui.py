# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'romlist.ui'
#
# Created: Tue Sep  3 02:08:52 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ROMList(object):
    def setupUi(self, ROMList):
        ROMList.setObjectName(_fromUtf8("ROMList"))
        ROMList.resize(850, 657)
        ROMList.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtGui.QWidget(ROMList)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupROMList = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupROMList.sizePolicy().hasHeightForWidth())
        self.groupROMList.setSizePolicy(sizePolicy)
        self.groupROMList.setAutoFillBackground(False)
        self.groupROMList.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex; \n"
" }\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; \n"
"    padding: 0 2px;\n"
" }"))
        self.groupROMList.setFlat(False)
        self.groupROMList.setCheckable(False)
        self.groupROMList.setObjectName(_fromUtf8("groupROMList"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupROMList)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(self.groupROMList)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.listWidget = QtGui.QListWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupTitle = QtGui.QGroupBox(self.layoutWidget)
        self.groupTitle.setAutoFillBackground(False)
        self.groupTitle.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex; \n"
" }\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; \n"
"    padding: 0 2px;\n"
" }"))
        self.groupTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.groupTitle.setFlat(False)
        self.groupTitle.setCheckable(False)
        self.groupTitle.setObjectName(_fromUtf8("groupTitle"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupTitle)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.titleView = ImageView(self.groupTitle)
        self.titleView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.titleView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.titleView.setBackgroundBrush(brush)
        self.titleView.setObjectName(_fromUtf8("titleView"))
        self.verticalLayout_3.addWidget(self.titleView)
        self.verticalLayout.addWidget(self.groupTitle)
        self.groupSnapshot = QtGui.QGroupBox(self.layoutWidget)
        self.groupSnapshot.setAutoFillBackground(False)
        self.groupSnapshot.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex; \n"
" }\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; \n"
"    padding: 0 2px;\n"
" }"))
        self.groupSnapshot.setAlignment(QtCore.Qt.AlignCenter)
        self.groupSnapshot.setFlat(False)
        self.groupSnapshot.setCheckable(False)
        self.groupSnapshot.setObjectName(_fromUtf8("groupSnapshot"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.groupSnapshot)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.snapshotView = ImageView(self.groupSnapshot)
        self.snapshotView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.snapshotView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.snapshotView.setBackgroundBrush(brush)
        self.snapshotView.setObjectName(_fromUtf8("snapshotView"))
        self.verticalLayout_10.addWidget(self.snapshotView)
        self.verticalLayout.addWidget(self.groupSnapshot)
        self.horizontalLayout.addWidget(self.splitter)
        self.verticalLayout_2.addWidget(self.groupROMList)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.checkAvailable = QtGui.QCheckBox(self.centralwidget)
        self.checkAvailable.setObjectName(_fromUtf8("checkAvailable"))
        self.horizontalLayout_7.addWidget(self.checkAvailable)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_7.addWidget(self.progressBar)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.pushRefresh = QtGui.QPushButton(self.centralwidget)
        self.pushRefresh.setEnabled(False)
        self.pushRefresh.setObjectName(_fromUtf8("pushRefresh"))
        self.horizontalLayout_6.addWidget(self.pushRefresh)
        self.labelAvailable = QtGui.QLabel(self.centralwidget)
        self.labelAvailable.setObjectName(_fromUtf8("labelAvailable"))
        self.horizontalLayout_6.addWidget(self.labelAvailable)
        spacerItem = QtGui.QSpacerItem(118, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        spacerItem1 = QtGui.QSpacerItem(488, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.pushCancel = QtGui.QPushButton(self.centralwidget)
        self.pushCancel.setAutoDefault(False)
        self.pushCancel.setObjectName(_fromUtf8("pushCancel"))
        self.horizontalLayout_8.addWidget(self.pushCancel)
        self.pushOpen = QtGui.QPushButton(self.centralwidget)
        self.pushOpen.setEnabled(False)
        self.pushOpen.setDefault(True)
        self.pushOpen.setObjectName(_fromUtf8("pushOpen"))
        self.horizontalLayout_8.addWidget(self.pushOpen)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        ROMList.setCentralWidget(self.centralwidget)

        self.retranslateUi(ROMList)
        QtCore.QObject.connect(self.pushCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), ROMList.close)
        QtCore.QMetaObject.connectSlotsByName(ROMList)

    def retranslateUi(self, ROMList):
        ROMList.setWindowTitle(_translate("ROMList", "Load ROM Image", None))
        self.groupROMList.setTitle(_translate("ROMList", "ROMs List", None))
        self.listWidget.setSortingEnabled(True)
        self.groupTitle.setTitle(_translate("ROMList", "Title Screen", None))
        self.groupSnapshot.setTitle(_translate("ROMList", "In Game Snapshot", None))
        self.checkAvailable.setText(_translate("ROMList", "Show available ROMs", None))
        self.pushRefresh.setText(_translate("ROMList", "Refresh", None))
        self.labelAvailable.setText(_translate("ROMList", "TextLabel", None))
        self.pushCancel.setText(_translate("ROMList", "&Cancel", None))
        self.pushOpen.setText(_translate("ROMList", "&Open", None))

from imageview import ImageView
