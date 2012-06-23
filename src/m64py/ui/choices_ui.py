# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choices.ui'
#
# Created: Sat Jun 23 10:26:17 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ChoicesDialog(object):
    def setupUi(self, ChoicesDialog):
        ChoicesDialog.setObjectName(_fromUtf8("ChoicesDialog"))
        ChoicesDialog.resize(274, 239)
        ChoicesDialog.setModal(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(ChoicesDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupChoices = QtGui.QGroupBox(ChoicesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupChoices.sizePolicy().hasHeightForWidth())
        self.groupChoices.setSizePolicy(sizePolicy)
        self.groupChoices.setAutoFillBackground(False)
        self.groupChoices.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupChoices.setTitle(_fromUtf8(""))
        self.groupChoices.setFlat(False)
        self.groupChoices.setCheckable(False)
        self.groupChoices.setObjectName(_fromUtf8("groupChoices"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupChoices)
        self.verticalLayout_2.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.groupChoices)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.labelName = QtGui.QLabel(self.groupChoices)
        self.labelName.setText(_fromUtf8(""))
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.verticalLayout_2.addWidget(self.labelName)
        self.scrollArea = QtGui.QScrollArea(self.groupChoices)
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
        self.verticalLayout_3.addWidget(self.groupChoices)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(228, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushOk = QtGui.QPushButton(ChoicesDialog)
        self.pushOk.setObjectName(_fromUtf8("pushOk"))
        self.horizontalLayout.addWidget(self.pushOk)
        self.pushCancel = QtGui.QPushButton(ChoicesDialog)
        self.pushCancel.setObjectName(_fromUtf8("pushCancel"))
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(ChoicesDialog)
        QtCore.QObject.connect(self.pushCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), ChoicesDialog.close)
        QtCore.QObject.connect(self.pushOk, QtCore.SIGNAL(_fromUtf8("clicked()")), ChoicesDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(ChoicesDialog)

    def retranslateUi(self, ChoicesDialog):
        ChoicesDialog.setWindowTitle(QtGui.QApplication.translate("ChoicesDialog", "Choices", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ChoicesDialog", "Choose a value to be used for:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushOk.setText(QtGui.QApplication.translate("ChoicesDialog", "&Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.pushCancel.setText(QtGui.QApplication.translate("ChoicesDialog", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))

