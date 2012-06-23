# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Sat Jun 23 10:26:18 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(509, 397)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Settings)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Settings)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.layoutWidget = QtGui.QWidget(self.tab_1)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 461, 271))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_13 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_13.setMargin(0)
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.groupLibrary = QtGui.QGroupBox(self.layoutWidget)
        self.groupLibrary.setAutoFillBackground(False)
        self.groupLibrary.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupLibrary.setFlat(False)
        self.groupLibrary.setCheckable(False)
        self.groupLibrary.setObjectName(_fromUtf8("groupLibrary"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupLibrary)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pathLibrary = QtGui.QLineEdit(self.groupLibrary)
        self.pathLibrary.setObjectName(_fromUtf8("pathLibrary"))
        self.horizontalLayout.addWidget(self.pathLibrary)
        self.browseLibrary = QtGui.QPushButton(self.groupLibrary)
        self.browseLibrary.setObjectName(_fromUtf8("browseLibrary"))
        self.horizontalLayout.addWidget(self.browseLibrary)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.verticalLayout_13.addWidget(self.groupLibrary)
        self.groupPlugins = QtGui.QGroupBox(self.layoutWidget)
        self.groupPlugins.setAutoFillBackground(False)
        self.groupPlugins.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupPlugins.setFlat(False)
        self.groupPlugins.setCheckable(False)
        self.groupPlugins.setObjectName(_fromUtf8("groupPlugins"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupPlugins)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.pathPlugins = QtGui.QLineEdit(self.groupPlugins)
        self.pathPlugins.setObjectName(_fromUtf8("pathPlugins"))
        self.horizontalLayout_7.addWidget(self.pathPlugins)
        self.browsePlugins = QtGui.QPushButton(self.groupPlugins)
        self.browsePlugins.setObjectName(_fromUtf8("browsePlugins"))
        self.horizontalLayout_7.addWidget(self.browsePlugins)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.verticalLayout_13.addWidget(self.groupPlugins)
        self.groupData = QtGui.QGroupBox(self.layoutWidget)
        self.groupData.setAutoFillBackground(False)
        self.groupData.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupData.setFlat(False)
        self.groupData.setCheckable(False)
        self.groupData.setObjectName(_fromUtf8("groupData"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.groupData)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pathData = QtGui.QLineEdit(self.groupData)
        self.pathData.setObjectName(_fromUtf8("pathData"))
        self.horizontalLayout_3.addWidget(self.pathData)
        self.browseData = QtGui.QPushButton(self.groupData)
        self.browseData.setObjectName(_fromUtf8("browseData"))
        self.horizontalLayout_3.addWidget(self.browseData)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.verticalLayout_13.addWidget(self.groupData)
        self.groupROM = QtGui.QGroupBox(self.layoutWidget)
        self.groupROM.setAutoFillBackground(False)
        self.groupROM.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupROM.setFlat(False)
        self.groupROM.setCheckable(False)
        self.groupROM.setObjectName(_fromUtf8("groupROM"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.groupROM)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.pathROM = QtGui.QLineEdit(self.groupROM)
        self.pathROM.setObjectName(_fromUtf8("pathROM"))
        self.horizontalLayout_4.addWidget(self.pathROM)
        self.browseROM = QtGui.QPushButton(self.groupROM)
        self.browseROM.setObjectName(_fromUtf8("browseROM"))
        self.horizontalLayout_4.addWidget(self.browseROM)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        self.verticalLayout_13.addWidget(self.groupROM)
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_14 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.groupGraphics = QtGui.QGroupBox(self.tab_2)
        self.groupGraphics.setAutoFillBackground(False)
        self.groupGraphics.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex; \n"
"    padding: 4px 0\n"
";\n"
" }\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; \n"
"    padding: 0 2px;\n"
" }"))
        self.groupGraphics.setFlat(False)
        self.groupGraphics.setCheckable(False)
        self.groupGraphics.setObjectName(_fromUtf8("groupGraphics"))
        self.verticalLayout_18 = QtGui.QVBoxLayout(self.groupGraphics)
        self.verticalLayout_18.setObjectName(_fromUtf8("verticalLayout_18"))
        self.verticalLayout_15 = QtGui.QVBoxLayout()
        self.verticalLayout_15.setObjectName(_fromUtf8("verticalLayout_15"))
        self.checkFullscreen = QtGui.QCheckBox(self.groupGraphics)
        self.checkFullscreen.setObjectName(_fromUtf8("checkFullscreen"))
        self.verticalLayout_15.addWidget(self.checkFullscreen)
        self.checkOSD = QtGui.QCheckBox(self.groupGraphics)
        self.checkOSD.setChecked(True)
        self.checkOSD.setObjectName(_fromUtf8("checkOSD"))
        self.verticalLayout_15.addWidget(self.checkOSD)
        self.checkEnableVidExt = QtGui.QCheckBox(self.groupGraphics)
        self.checkEnableVidExt.setChecked(False)
        self.checkEnableVidExt.setObjectName(_fromUtf8("checkEnableVidExt"))
        self.verticalLayout_15.addWidget(self.checkEnableVidExt)
        self.groupResolution = QtGui.QGroupBox(self.groupGraphics)
        self.groupResolution.setAutoFillBackground(False)
        self.groupResolution.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupResolution.setFlat(False)
        self.groupResolution.setCheckable(False)
        self.groupResolution.setObjectName(_fromUtf8("groupResolution"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.groupResolution)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.comboResolution = QtGui.QComboBox(self.groupResolution)
        self.comboResolution.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboResolution.sizePolicy().hasHeightForWidth())
        self.comboResolution.setSizePolicy(sizePolicy)
        self.comboResolution.setObjectName(_fromUtf8("comboResolution"))
        self.horizontalLayout_10.addWidget(self.comboResolution)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.verticalLayout_11.addLayout(self.horizontalLayout_10)
        self.verticalLayout_15.addWidget(self.groupResolution)
        self.verticalLayout_18.addLayout(self.verticalLayout_15)
        self.verticalLayout_10.addWidget(self.groupGraphics)
        self.groupEmuMode = QtGui.QGroupBox(self.tab_2)
        self.groupEmuMode.setAutoFillBackground(False)
        self.groupEmuMode.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex;\n"
"    padding: 4px 0;\n"
" }\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; \n"
"    padding: 0 2px;\n"
" }"))
        self.groupEmuMode.setFlat(False)
        self.groupEmuMode.setCheckable(False)
        self.groupEmuMode.setObjectName(_fromUtf8("groupEmuMode"))
        self.verticalLayout_10.addWidget(self.groupEmuMode)
        self.groupEmuMode_2 = QtGui.QGroupBox(self.tab_2)
        self.groupEmuMode_2.setAutoFillBackground(False)
        self.groupEmuMode_2.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex;\n"
"    padding: 4px 0;\n"
" }\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; \n"
"    padding: 0 2px;\n"
" }"))
        self.groupEmuMode_2.setFlat(False)
        self.groupEmuMode_2.setCheckable(False)
        self.groupEmuMode_2.setObjectName(_fromUtf8("groupEmuMode_2"))
        self.verticalLayout_17 = QtGui.QVBoxLayout(self.groupEmuMode_2)
        self.verticalLayout_17.setObjectName(_fromUtf8("verticalLayout_17"))
        self.verticalLayout_16 = QtGui.QVBoxLayout()
        self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
        self.checkNoCompiledJump = QtGui.QCheckBox(self.groupEmuMode_2)
        self.checkNoCompiledJump.setObjectName(_fromUtf8("checkNoCompiledJump"))
        self.verticalLayout_16.addWidget(self.checkNoCompiledJump)
        self.checkDisableExtraMem = QtGui.QCheckBox(self.groupEmuMode_2)
        self.checkDisableExtraMem.setObjectName(_fromUtf8("checkDisableExtraMem"))
        self.verticalLayout_16.addWidget(self.checkDisableExtraMem)
        self.verticalLayout_17.addLayout(self.verticalLayout_16)
        self.verticalLayout_10.addWidget(self.groupEmuMode_2)
        self.verticalLayout_14.addLayout(self.verticalLayout_10)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.layoutWidget1 = QtGui.QWidget(self.tab_3)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 461, 271))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_12.setMargin(0)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.groupVideo = QtGui.QGroupBox(self.layoutWidget1)
        self.groupVideo.setAutoFillBackground(False)
        self.groupVideo.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupVideo.setFlat(False)
        self.groupVideo.setCheckable(False)
        self.groupVideo.setObjectName(_fromUtf8("groupVideo"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupVideo)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtGui.QLabel(self.groupVideo)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/plugins_video.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        self.comboVideo = QtGui.QComboBox(self.groupVideo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboVideo.sizePolicy().hasHeightForWidth())
        self.comboVideo.setSizePolicy(sizePolicy)
        self.comboVideo.setObjectName(_fromUtf8("comboVideo"))
        self.horizontalLayout_5.addWidget(self.comboVideo)
        self.pushButtonVideo = QtGui.QPushButton(self.groupVideo)
        self.pushButtonVideo.setEnabled(False)
        self.pushButtonVideo.setObjectName(_fromUtf8("pushButtonVideo"))
        self.horizontalLayout_5.addWidget(self.pushButtonVideo)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_12.addWidget(self.groupVideo)
        self.groupAudio = QtGui.QGroupBox(self.layoutWidget1)
        self.groupAudio.setAutoFillBackground(False)
        self.groupAudio.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupAudio.setFlat(False)
        self.groupAudio.setCheckable(False)
        self.groupAudio.setObjectName(_fromUtf8("groupAudio"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupAudio)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_2 = QtGui.QLabel(self.groupAudio)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/plugins_audio.png")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_6.addWidget(self.label_2)
        self.comboAudio = QtGui.QComboBox(self.groupAudio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboAudio.sizePolicy().hasHeightForWidth())
        self.comboAudio.setSizePolicy(sizePolicy)
        self.comboAudio.setObjectName(_fromUtf8("comboAudio"))
        self.horizontalLayout_6.addWidget(self.comboAudio)
        self.pushButtonAudio = QtGui.QPushButton(self.groupAudio)
        self.pushButtonAudio.setEnabled(False)
        self.pushButtonAudio.setObjectName(_fromUtf8("pushButtonAudio"))
        self.horizontalLayout_6.addWidget(self.pushButtonAudio)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_12.addWidget(self.groupAudio)
        self.groupInput = QtGui.QGroupBox(self.layoutWidget1)
        self.groupInput.setAutoFillBackground(False)
        self.groupInput.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupInput.setFlat(False)
        self.groupInput.setCheckable(False)
        self.groupInput.setObjectName(_fromUtf8("groupInput"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupInput)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_3 = QtGui.QLabel(self.groupInput)
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/plugins_input.png")))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_8.addWidget(self.label_3)
        self.comboInput = QtGui.QComboBox(self.groupInput)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboInput.sizePolicy().hasHeightForWidth())
        self.comboInput.setSizePolicy(sizePolicy)
        self.comboInput.setObjectName(_fromUtf8("comboInput"))
        self.horizontalLayout_8.addWidget(self.comboInput)
        self.pushButtonInput = QtGui.QPushButton(self.groupInput)
        self.pushButtonInput.setEnabled(False)
        self.pushButtonInput.setObjectName(_fromUtf8("pushButtonInput"))
        self.horizontalLayout_8.addWidget(self.pushButtonInput)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.verticalLayout_12.addWidget(self.groupInput)
        self.groupRSP = QtGui.QGroupBox(self.layoutWidget1)
        self.groupRSP.setAutoFillBackground(False)
        self.groupRSP.setStyleSheet(_fromUtf8("QGroupBox {\n"
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
        self.groupRSP.setFlat(False)
        self.groupRSP.setCheckable(False)
        self.groupRSP.setObjectName(_fromUtf8("groupRSP"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupRSP)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_4 = QtGui.QLabel(self.groupRSP)
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/plugins_rsp.png")))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_9.addWidget(self.label_4)
        self.comboRSP = QtGui.QComboBox(self.groupRSP)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboRSP.sizePolicy().hasHeightForWidth())
        self.comboRSP.setSizePolicy(sizePolicy)
        self.comboRSP.setObjectName(_fromUtf8("comboRSP"))
        self.horizontalLayout_9.addWidget(self.comboRSP)
        self.pushButtonRSP = QtGui.QPushButton(self.groupRSP)
        self.pushButtonRSP.setEnabled(False)
        self.pushButtonRSP.setObjectName(_fromUtf8("pushButtonRSP"))
        self.horizontalLayout_9.addWidget(self.pushButtonRSP)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.verticalLayout_12.addWidget(self.groupRSP)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(368, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.closeButton = QtGui.QPushButton(Settings)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Settings)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Settings.close)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QtGui.QApplication.translate("Settings", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupLibrary.setTitle(QtGui.QApplication.translate("Settings", "Library file", None, QtGui.QApplication.UnicodeUTF8))
        self.browseLibrary.setText(QtGui.QApplication.translate("Settings", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.groupPlugins.setTitle(QtGui.QApplication.translate("Settings", "Plugins directory", None, QtGui.QApplication.UnicodeUTF8))
        self.browsePlugins.setText(QtGui.QApplication.translate("Settings", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.groupData.setTitle(QtGui.QApplication.translate("Settings", "Data directory", None, QtGui.QApplication.UnicodeUTF8))
        self.browseData.setText(QtGui.QApplication.translate("Settings", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.groupROM.setTitle(QtGui.QApplication.translate("Settings", "ROMs directory", None, QtGui.QApplication.UnicodeUTF8))
        self.browseROM.setText(QtGui.QApplication.translate("Settings", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QtGui.QApplication.translate("Settings", "Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.groupGraphics.setTitle(QtGui.QApplication.translate("Settings", "Graphics", None, QtGui.QApplication.UnicodeUTF8))
        self.checkFullscreen.setText(QtGui.QApplication.translate("Settings", "Fullscreen", None, QtGui.QApplication.UnicodeUTF8))
        self.checkOSD.setText(QtGui.QApplication.translate("Settings", "On Screen Display", None, QtGui.QApplication.UnicodeUTF8))
        self.checkEnableVidExt.setToolTip(QtGui.QApplication.translate("Settings", "<html><head/><body><p>Enable embedding of OpenGL window. This option needs restart.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkEnableVidExt.setText(QtGui.QApplication.translate("Settings", "Enable Video Extension", None, QtGui.QApplication.UnicodeUTF8))
        self.groupResolution.setTitle(QtGui.QApplication.translate("Settings", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
        self.comboResolution.setToolTip(QtGui.QApplication.translate("Settings", "Used only when video extension is not enabled", None, QtGui.QApplication.UnicodeUTF8))
        self.groupEmuMode.setTitle(QtGui.QApplication.translate("Settings", "CPU Core", None, QtGui.QApplication.UnicodeUTF8))
        self.groupEmuMode_2.setTitle(QtGui.QApplication.translate("Settings", "Compatibility", None, QtGui.QApplication.UnicodeUTF8))
        self.checkNoCompiledJump.setText(QtGui.QApplication.translate("Settings", "No Compiled Jump", None, QtGui.QApplication.UnicodeUTF8))
        self.checkDisableExtraMem.setText(QtGui.QApplication.translate("Settings", "Disable Extra Memory", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Settings", "Emulator", None, QtGui.QApplication.UnicodeUTF8))
        self.groupVideo.setTitle(QtGui.QApplication.translate("Settings", "Video", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonVideo.setText(QtGui.QApplication.translate("Settings", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.groupAudio.setTitle(QtGui.QApplication.translate("Settings", "Audio", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAudio.setText(QtGui.QApplication.translate("Settings", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.groupInput.setTitle(QtGui.QApplication.translate("Settings", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonInput.setText(QtGui.QApplication.translate("Settings", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.groupRSP.setTitle(QtGui.QApplication.translate("Settings", "Rsp", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRSP.setText(QtGui.QApplication.translate("Settings", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Settings", "Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("Settings", "&Close", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
