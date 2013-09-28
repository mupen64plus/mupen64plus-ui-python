# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'archive.ui'
#
# Created: Tue Sep  3 02:08:51 2013
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

class Ui_ArchiveDialog(object):
    def setupUi(self, ArchiveDialog):
        ArchiveDialog.setObjectName(_fromUtf8("ArchiveDialog"))
        ArchiveDialog.resize(274, 224)
        ArchiveDialog.setModal(False)
        self.verticalLayout_3 = QtGui.QVBoxLayout(ArchiveDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.fileChoices = QtGui.QGroupBox(ArchiveDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileChoices.sizePolicy().hasHeightForWidth())
        self.fileChoices.setSizePolicy(sizePolicy)
        self.fileChoices.setAutoFillBackground(False)
        self.fileChoices.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.fileChoices.setTitle(_fromUtf8(""))
        self.fileChoices.setFlat(False)
        self.fileChoices.setCheckable(False)
        self.fileChoices.setObjectName(_fromUtf8("fileChoices"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.fileChoices)
        self.verticalLayout_2.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.fileChoices)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.scrollArea = QtGui.QScrollArea(self.fileChoices)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 232, 120))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidget = QtGui.QListWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout_3.addWidget(self.fileChoices)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(228, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushOk = QtGui.QPushButton(ArchiveDialog)
        self.pushOk.setObjectName(_fromUtf8("pushOk"))
        self.horizontalLayout.addWidget(self.pushOk)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(ArchiveDialog)
        self.listWidget.setCurrentRow(-1)
        QtCore.QObject.connect(self.pushOk, QtCore.SIGNAL(_fromUtf8("clicked()")), ArchiveDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(ArchiveDialog)

    def retranslateUi(self, ArchiveDialog):
        ArchiveDialog.setWindowTitle(_translate("ArchiveDialog", "Archive", None))
        self.label.setText(_translate("ArchiveDialog", "Choose a file from archive:", None))
        self.pushOk.setText(_translate("ArchiveDialog", "&Ok", None))

