from Qt import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
import os
import json
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQWidgetBaseMixin, MayaQDockWidget

from Qt.QtWidgets import QMainWindow, QMenu

import logging
from new_set import*
from group import*

ROOT  = str(os.path.dirname(__file__))


class I_Select_GUI(MayaQWidgetDockableMixin, QtWidgets.QDockWidget):

    ### Defining our QT widget workspace and icons ###

    def __init__(self):

        super (I_Select_GUI, self).__init__()

        self.setMinimumSize(320, 400)                # Widget size
        self.setObjectName('GUI_object')             # widget's object name
        self.setWindowTitle("I Select")              # main window title
        self.setDockableParameters(width = 320)      # dockable width

        self.mainWidget = QtWidgets.QWidget()       # main widget
        self.setWidget(self.mainWidget)              # setting self.mainWidget as main

        self.gui_layout = QtWidgets.QVBoxLayout()    # main widget layout
        self.mainWidget.setLayout(self.gui_layout)   # layout for mainWidget
        self.gui_layout.setContentsMargins(1,1,1,1)  # margings for main layout

        self.menu_group = QtWidgets.QGroupBox()      # creating menu group
        self.menu_group.setMaximumHeight(50)         # height for menu group

                                                     # buttons 
        self.openButton = QtWidgets.QPushButton()    # open set button
        self.openButton.setFixedSize(32, 32)
        self.openButton.setIcon(QtGui.QIcon
                               (os.path.join
                               (ROOT, "icons", "open.svg")))
        self.openButton.setIconSize(QtCore.QSize(32,32))
        self.openButton.setFlat(True)                       
        
        self.saveButton = QtWidgets.QPushButton()    # save set button
        self.saveButton.setFixedSize(32,32)
        self.saveButton.setFlat(True)
        self.saveButton.setIcon(QtGui.QIcon
                               (os.path.join
                               (ROOT, "icons", "save.svg")))
        self.saveButton.setIconSize(QtCore.QSize(32,32))

        self.groupButton = QtWidgets.QPushButton()   # new group button
        self.groupButton.setFixedSize(32,32)
        self.groupButton.setFlat(True)
        self.groupButton.setIcon(QtGui.QIcon
                                (os.path.join
                                (ROOT, "icons", "new_group.svg")))
        self.groupButton.setIconSize(QtCore.QSize(32,32))

        self.setButton = QtWidgets.QPushButton()     # new set button
        self.setButton.setFixedSize(32,32)
        self.setButton.setFlat(True)
        self.setButton.setIcon(QtGui.QIcon
                              (os.path.join
                              (ROOT, "icons", "new_set.svg")))
        self.setButton.setIconSize(QtCore.QSize(32,32))                       
                                            
        self.menuLayout = QtWidgets.QHBoxLayout()      # layout for buttons
        self.menuLayout.addWidget(self.openButton)
        self.menuLayout.addWidget(self.saveButton)
        self.menuLayout.addWidget(self.groupButton)
        self.menuLayout.addWidget(self.setButton)

        self.menu_group.setLayout(self.menuLayout)   # adding menu layout to menu group
        self.gui_layout.addWidget(self.menu_group)   # adding menu group to gui main layout
        
        self.gui_layout.setAlignment(self.menu_group, QtCore.Qt.AlignTop)  # align menu group to the top

        
        ### creating scroll area for new selection sets ###
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setMinimumHeight(200)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.scrollArea_Widget = QtWidgets.QWidget()         # making widget for scroll area
        self.scrollArea.setWidget(self.scrollArea_Widget)

        self.scroll_layout = QtWidgets.QGridLayout()         # layout for scroll area
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)  # making top alignment in scroll area
        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.scroll_layout.setSpacing(5)                     # spacing between objects in scroll layout

        self.scrollArea_Widget.setLayout(self.scroll_layout) # setting scroll layout for scroll area Widget

        self.gui_layout.addWidget(self.scrollArea)           # adding scroll area to main gui widget


        ###########################################
        ### connecting GUI buttons to functions ###
        ###########################################

        self.setButton.clicked.connect(self.new_set_button_clicked)
        self.groupButton.clicked.connect(self.new_group_button_clicked)
        self.openButton.clicked.connect(self.open_saved_set)
        self.saveButton.clicked.connect(self.save_created_set)

    ##############################################
    ### functions related to GUI Buttons #########
    ##############################################
    
    def new_set_button_clicked(self):
        logging.info("New Selection Set has been created")
        NewSet = CustomSet()
        self.scroll_layout.addWidget(NewSet)

    def new_group_button_clicked(self):
        logging.info("New Group has been created")
        Group = NewGroup()
        self.scroll_layout.addWidget(Group)

    def open_saved_set(self):
        logging.info("Set has been opened")

    def save_created_set(self):
        logging.info("Your set has been saved")            


# deleting GUI interface before opening new
def deleteGUI(control):

    if cmds.workspaceControl(control, q = True, exists = True):
        cmds.workspaceControl(control, e = True, close = True)

        cmds.deleteUI(control, control = True) 
        logging.info("I Select has been deleted and reopened")       

    else:

        logging.info("I select has been opened")

# running gui function
def runGUI():

    deleteGUI("GUI_objectWorkspaceControl")

    dialog = I_Select_GUI()
    dialog.show(dockable = True, floating = True)
    
    cmds.workspaceControl("GUI_objectWorkspaceControl", e = True, wp = 320) 
    dialog.raise_() 
       
             
        