# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cheat.ui'
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

class Ui_CheatDialog(object):
    def setupUi(self, CheatDialog):
        CheatDialog.setObjectName(_fromUtf8("CheatDialog"))
        CheatDialog.resize(350, 382)
        self.verticalLayout_3 = QtGui.QVBoxLayout(CheatDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupCheats = QtGui.QGroupBox(CheatDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupCheats.sizePolicy().hasHeightForWidth())
        self.groupCheats.setSizePolicy(sizePolicy)
        self.groupCheats.setMinimumSize(QtCore.QSize(0, 0))
        self.groupCheats.setAutoFillBackground(False)
        self.groupCheats.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupCheats.setFlat(False)
        self.groupCheats.setCheckable(False)
        self.groupCheats.setObjectName(_fromUtf8("groupCheats"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupCheats)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeWidget = QtGui.QTreeWidget(self.groupCheats)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)
        self.verticalLayout_3.addWidget(self.groupCheats)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(208, 18, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushUnmarkAll = QtGui.QPushButton(CheatDialog)
        self.pushUnmarkAll.setObjectName(_fromUtf8("pushUnmarkAll"))
        self.horizontalLayout_2.addWidget(self.pushUnmarkAll)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.groupNotes = QtGui.QGroupBox(CheatDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupNotes.sizePolicy().hasHeightForWidth())
        self.groupNotes.setSizePolicy(sizePolicy)
        self.groupNotes.setMinimumSize(QtCore.QSize(0, 75))
        self.groupNotes.setAutoFillBackground(False)
        self.groupNotes.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupNotes.setFlat(False)
        self.groupNotes.setCheckable(False)
        self.groupNotes.setObjectName(_fromUtf8("groupNotes"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupNotes)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea_2 = QtGui.QScrollArea(self.groupNotes)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        self.scrollArea_2.setStyleSheet(_fromUtf8("background: #FFF;"))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 308, 44))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.labelDesc = QtGui.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDesc.sizePolicy().hasHeightForWidth())
        self.labelDesc.setSizePolicy(sizePolicy)
        self.labelDesc.setText(_fromUtf8(""))
        self.labelDesc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelDesc.setWordWrap(True)
        self.labelDesc.setObjectName(_fromUtf8("labelDesc"))
        self.verticalLayout_4.addWidget(self.labelDesc)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea_2)
        self.verticalLayout_3.addWidget(self.groupNotes)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(228, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushClose = QtGui.QPushButton(CheatDialog)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.horizontalLayout.addWidget(self.pushClose)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(CheatDialog)
        QtCore.QObject.connect(self.pushClose, QtCore.SIGNAL(_fromUtf8("clicked()")), CheatDialog.hide)
        QtCore.QMetaObject.connectSlotsByName(CheatDialog)

    def retranslateUi(self, CheatDialog):
        CheatDialog.setWindowTitle(_translate("CheatDialog", "Cheats", None))
        self.groupCheats.setTitle(_translate("CheatDialog", "Cheats", None))
        self.pushUnmarkAll.setText(_translate("CheatDialog", "Unmark All", None))
        self.groupNotes.setTitle(_translate("CheatDialog", "Notes", None))
        self.pushClose.setText(_translate("CheatDialog", "&Close", None))

