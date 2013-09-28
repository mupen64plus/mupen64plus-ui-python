# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
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

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(507, 392)
        self.verticalLayout_14 = QtGui.QVBoxLayout(Settings)
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.tabWidget = QtGui.QTabWidget(Settings)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.layoutWidget = QtGui.QWidget(self.tab_1)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 271))
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
        self.widget = QtGui.QWidget(self.tab_2)
        self.widget.setGeometry(QtCore.QRect(10, 10, 461, 211))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_10.setMargin(0)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.groupEmuMode = QtGui.QGroupBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupEmuMode.sizePolicy().hasHeightForWidth())
        self.groupEmuMode.setSizePolicy(sizePolicy)
        self.groupEmuMode.setAutoFillBackground(False)
        self.groupEmuMode.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex;\n"
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
        self.groupEmuMode_2 = QtGui.QGroupBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupEmuMode_2.sizePolicy().hasHeightForWidth())
        self.groupEmuMode_2.setSizePolicy(sizePolicy)
        self.groupEmuMode_2.setAutoFillBackground(False)
        self.groupEmuMode_2.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex;\n"
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
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.widget1 = QtGui.QWidget(self.tab_4)
        self.widget1.setGeometry(QtCore.QRect(11, 10, 461, 233))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_18 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_18.setMargin(0)
        self.verticalLayout_18.setObjectName(_fromUtf8("verticalLayout_18"))
        self.groupGraphics = QtGui.QGroupBox(self.widget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupGraphics.sizePolicy().hasHeightForWidth())
        self.groupGraphics.setSizePolicy(sizePolicy)
        self.groupGraphics.setAutoFillBackground(False)
        self.groupGraphics.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex;\n"
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
        self.verticalLayout_15 = QtGui.QVBoxLayout(self.groupGraphics)
        self.verticalLayout_15.setSpacing(6)
        self.verticalLayout_15.setObjectName(_fromUtf8("verticalLayout_15"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.checkOSD = QtGui.QCheckBox(self.groupGraphics)
        self.checkOSD.setChecked(True)
        self.checkOSD.setObjectName(_fromUtf8("checkOSD"))
        self.verticalLayout_2.addWidget(self.checkOSD)
        self.checkDisableScreenSaver = QtGui.QCheckBox(self.groupGraphics)
        self.checkDisableScreenSaver.setObjectName(_fromUtf8("checkDisableScreenSaver"))
        self.verticalLayout_2.addWidget(self.checkDisableScreenSaver)
        self.checkEnableVidExt = QtGui.QCheckBox(self.groupGraphics)
        self.checkEnableVidExt.setChecked(False)
        self.checkEnableVidExt.setObjectName(_fromUtf8("checkEnableVidExt"))
        self.verticalLayout_2.addWidget(self.checkEnableVidExt)
        self.checkKeepAspect = QtGui.QCheckBox(self.groupGraphics)
        self.checkKeepAspect.setObjectName(_fromUtf8("checkKeepAspect"))
        self.verticalLayout_2.addWidget(self.checkKeepAspect)
        self.verticalLayout_15.addLayout(self.verticalLayout_2)
        self.verticalLayout_18.addWidget(self.groupGraphics)
        self.groupResolution = QtGui.QGroupBox(self.widget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupResolution.sizePolicy().hasHeightForWidth())
        self.groupResolution.setSizePolicy(sizePolicy)
        self.groupResolution.setAutoFillBackground(False)
        self.groupResolution.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid #7F7F7F;\n"
"    border-radius: 3px;\n"
"    margin-top: 1ex;\n"
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
        self.checkFullscreen = QtGui.QCheckBox(self.groupResolution)
        self.checkFullscreen.setChecked(False)
        self.checkFullscreen.setObjectName(_fromUtf8("checkFullscreen"))
        self.verticalLayout_11.addWidget(self.checkFullscreen)
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
        self.verticalLayout_18.addWidget(self.groupResolution)
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
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
        self.verticalLayout_14.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(368, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.closeButton = QtGui.QPushButton(Settings)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout_14.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Settings)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Settings.close)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "Settings", None))
        self.groupLibrary.setTitle(_translate("Settings", "Library file", None))
        self.browseLibrary.setText(_translate("Settings", "Browse", None))
        self.groupPlugins.setTitle(_translate("Settings", "Plugins directory", None))
        self.browsePlugins.setText(_translate("Settings", "Browse", None))
        self.groupData.setTitle(_translate("Settings", "Data directory", None))
        self.browseData.setText(_translate("Settings", "Browse", None))
        self.groupROM.setTitle(_translate("Settings", "ROMs directory", None))
        self.browseROM.setText(_translate("Settings", "Browse", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Settings", "Paths", None))
        self.groupEmuMode.setTitle(_translate("Settings", "CPU Core", None))
        self.groupEmuMode_2.setTitle(_translate("Settings", "Compatibility", None))
        self.checkNoCompiledJump.setText(_translate("Settings", "No Compiled Jump", None))
        self.checkDisableExtraMem.setText(_translate("Settings", "Disable Extra Memory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Settings", "Emulator", None))
        self.groupGraphics.setTitle(_translate("Settings", "Graphics", None))
        self.checkOSD.setText(_translate("Settings", "On Screen Display", None))
        self.checkDisableScreenSaver.setToolTip(_translate("Settings", "Disables ScreenSaver when emulator is running", None))
        self.checkDisableScreenSaver.setText(_translate("Settings", "Disable ScreenSaver", None))
        self.checkEnableVidExt.setToolTip(_translate("Settings", "Enable embedding of OpenGL window. This option needs restart.", None))
        self.checkEnableVidExt.setText(_translate("Settings", "Enable Video Extension", None))
        self.checkKeepAspect.setToolTip(_translate("Settings", "Maintain aspect-ratio on resizing", None))
        self.checkKeepAspect.setText(_translate("Settings", "Keep Aspect Ratio", None))
        self.groupResolution.setTitle(_translate("Settings", "Resolution", None))
        self.checkFullscreen.setToolTip(_translate("Settings", "Fullscreen, used only when video extension is disabled", None))
        self.checkFullscreen.setText(_translate("Settings", "Fullscreen", None))
        self.comboResolution.setToolTip(_translate("Settings", "Used only when video extension is disabled", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Settings", "Graphics", None))
        self.groupVideo.setTitle(_translate("Settings", "Video", None))
        self.pushButtonVideo.setText(_translate("Settings", "Configure", None))
        self.groupAudio.setTitle(_translate("Settings", "Audio", None))
        self.pushButtonAudio.setText(_translate("Settings", "Configure", None))
        self.groupInput.setTitle(_translate("Settings", "Input", None))
        self.pushButtonInput.setText(_translate("Settings", "Configure", None))
        self.groupRSP.setTitle(_translate("Settings", "Rsp", None))
        self.pushButtonRSP.setText(_translate("Settings", "Configure", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Settings", "Plugins", None))
        self.closeButton.setText(_translate("Settings", "&Close", None))

import icons_rc
