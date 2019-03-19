from Qt import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
import os
import json
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQWidgetBaseMixin, MayaQDockWidget

from Qt.QtWidgets import QMainWindow, QMenu

import logging

ROOT  = str(os.path.dirname(__file__))

class NewGroup(QtWidgets.QWidget):

    ################################
    ### group for nested sets ######
    ################################

    def __init__(self):
        super(NewGroup, self).__init__()

        # adding main layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setObjectName("New_Group")
        self.setMinimumHeight(40)       
        self.mainLayout.setSpacing(5)
        self.mainLayout.setContentsMargins(1,1,1,1)
        
        # group and layout for label and open/close button
        self.label_group = QtWidgets.QGroupBox()
        self.group_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(1,1,1,1)

        self.label_group.setLayout(self.group_layout)
        
        self.mainLayout.addWidget(self.label_group)
        self.mainLayout.setAlignment(self.label_group, QtCore.Qt.AlignTop)

        #adding small opener icon to open/close group
        self.smallBox = QtWidgets.QPushButton()
        self.smallBox.setFlat(True)
        self.smallBox.setFixedSize(18,18)
        self.smallBox.setStyleSheet("QPushButton:checked{background-color: transparent; color: black; border: black 2px; }"
                                    "QPushButton:pressed{background-color: transparent; color: black; border: black 2px; }")
        
        self.openIcon = QtGui.QIcon(os.path.join(ROOT, "icons", "groupOpen.svg"))
        self.closeIcon = QtGui.QIcon(os.path.join(ROOT, "icons", "groupClose.svg"))

        self.smallBox.setIcon(self.openIcon)
        self.smallBox.setIconSize(QtCore.QSize(18,18))
        self.smallBox.toggle()
        self.smallBox.setCheckable(True)

        self.group_layout.addWidget(self.smallBox)

        #setting group label
        self.groupName = QtWidgets.QLabel("Group")
        self.group_layout.addWidget(self.groupName)
        self.font = QtGui.QFont("Arial", 10)
        self.groupName.setFont(self.font)


        # color
        self.bgcolor = 75
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(self.bgcolor,self.bgcolor,self.bgcolor))
        self.setPalette(self.p)

        
        
        
        
        
        #########################
        ## connect to functions##
        #########################
        self.smallBox.clicked.connect(self.open_close_group)

        
        

    def open_close_group(self):
        
        if self.smallBox.isChecked():
            print("Hello")
            self.smallBox.setIcon(self.closeIcon)
        else:
            self.smallBox.setIcon(self.openIcon)    




