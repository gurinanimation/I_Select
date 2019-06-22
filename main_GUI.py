# Quick selection sets for Maya with drag and drop function.
# Made by Ihor Hurin  gurin.animation@gmail.com

import sys
from Qt import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
import os
import json
import re
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQWidgetBaseMixin, MayaQDockWidget

from Qt.QtWidgets import QMainWindow, QMenu

import logging
import new_set as ns
import group as ng

ROOT  = str(os.path.dirname(__file__))

class I_Select_GUI(MayaQWidgetDockableMixin, QtWidgets.QDockWidget):

    ### Defining our QT widget workspace and icons ###

    def __init__(self):

        super (I_Select_GUI, self).__init__()

        self.counter = 0                            # counter variable for new set suffix
        self.group_label_name = "Group_"            # variable - new group prefix
        self.set_label_name = "Set_"                # variable - new set prefix
                
        ###########################################################################
        self.setMinimumSize(320, 350)                # Widget size
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
        self.saveButton.setIconSize(QtCore.QSize(32, 32))

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

        self.setButton.clicked.connect(self.new_set_button_clicked)
        self.groupButton.clicked.connect(self.new_group_button_clicked)
        self.openButton.clicked.connect(self.open_saved_set)
        self.saveButton.clicked.connect(self.save_created_set)

        ### accepting drops for drag and drop ###
        self.setAcceptDrops(True)

    ##############################################
    ### functions related to GUI Buttons #########
    
    # function to add new sets to scroll_layout
    def new_set_button_clicked(self):                      
                
        self.counter += 1
        NewSet = ns.CustomSet(labelName = self.set_label_name + str(self.counter))
        self.scroll_layout.addWidget(NewSet)
        NewSet.deleteScrollPressed.connect(self.delete_selected_widget)
        sys.stdout.write("New set has been created")

    # function to add new groups to scroll_layout
    def new_group_button_clicked(self):
        
        self.counter += 1
        Group = ng.NewGroup(labelName = self.group_label_name + str(self.counter))                                  
        self.scroll_layout.addWidget(Group)
        Group.deletePressed.connect(self.delete_selected_widget)
        sys.stdout.write("New group has been created")
          
    # function to delete groups/sets from scroll_layout
    def delete_selected_widget(self, labelName = None ):
        if not labelName:
            return

        elif self.scroll_layout.count() > 0:
            for i in range(0, self.scroll_layout.count()):
                item = self.scroll_layout.itemAt(i)
                itemWidget = item.widget()
                if itemWidget.labelName == labelName:
                    itemWidget.deleteLater()                
    
    #### functions to open saved json set ###
    def add_group_from_json(self, group = None):
        if self.scroll_layout.count() > 0:
            for i in range(0, self.scroll_layout.count()):
                item = self.scroll_layout.itemAt(i)
                itemWidget = item.widget()
                labelName = itemWidget.labelName
                ImportedName = group.labelName               
                if str(ImportedName) == str(labelName):
                    return -1
            
        self.scroll_layout.addWidget(group) 

    def add_set_from_json(self, selSet = None, layout = None):
        
        if layout == "scroll":
            if self.scroll_layout.count() > 0:
                for i in range(0, self.scroll_layout.count()):
                    item = self.scroll_layout.itemAt(i)
                    itemWidget = item.widget()
                    if itemWidget == selSet:
                        return
            self.scroll_layout.addWidget(selSet)

        else:
            if self.scroll_layout.count() > 0:
                for i in range(0, self.scroll_layout.count()):
                    item = self.scroll_layout.itemAt(i)
                    itemWidget = item.widget()
                    GroupName = itemWidget.labelName
                    
                    if GroupName == layout:
                        height = itemWidget.drop.height()
                        itemWidget.drop.setFixedHeight(height + 45)
                        groupLayout = itemWidget.drop.drop_layout
                        groupLayout.addWidget(selSet)
                        selSet.deleteScrollPressed.connect(itemWidget.drop.delete_selected_widget)

                        
                        
    def open_saved_set(self, openName = None):
        
        # open json file
        if not openName: 
            basicFilter = "*.json"
            returnData  = cmds.fileDialog2(dialogStyle = 2, fm = 1, ff = basicFilter)
            openName = returnData[0]
        
        with open(openName, "r") as data:
            sets = json.load(data)
        
        # reading dictionaries from json

        for i in sets["sets"]:
            if "Group" in i:

                groupName = i["Group"]
                groupSetName = i["Name"]
                groupSetColor = i["Color"]
                groupSetObjects = i["Objects"]

                Group = ng.NewGroup(labelName = groupName)
                Group.deletePressed.connect(self.delete_selected_widget)
                runGroup = self.add_group_from_json(group = Group)

                widget = ns.CustomSet(labelName = groupSetName, color = groupSetColor)
                widget.stored_selection = groupSetObjects
                
                runGroupSet = self.add_set_from_json(selSet = widget, layout = groupName)

            else:
                setName = i["Name"]
                setColor = i["Color"]
                setObjects = i["Objects"]
                widget = ns.CustomSet(labelName = setName, color = setColor)
                widget.stored_selection = setObjects
                widget.deleteScrollPressed.connect(self.delete_selected_widget)
                
                runSet = self.add_set_from_json(selSet = widget, layout = "scroll")   

        sys.stdout.write("Set has been opened")
       
    # function to save set into json file
    def save_created_set(self, fileName = None):
        self.data = {"sets": []}
         
        # getting dictionaries from layouts and groups with sets
        for i in range(0, self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            widget = item.widget()
            x = str(widget)
             
            if "CustomSet" in x:
                setDict = {"Name": None, "Color": None, "Objects": None}
                
                #getting widget's name
                name = widget.labelName
                
                #getting widget's color
                color = widget.saveColorJson
                print(color)            
                
                #getting widget's objects stored in set
                objects = widget.stored_selection

                # adding all variables to temporary Dictionary
                setDict["Name"] = name
                setDict["Color"] = color
                setDict["Objects"] = objects

                self.data["sets"].append(setDict)

            if "NewGroup" in x:

                for i in range(0, widget.drop.drop_layout.count()):

                    groupDict = {"Group": None, "Name": None, "Color": None, "Objects": None}
                    
                    groupItem = widget.drop.drop_layout.itemAt(i)
                    groupWidget = groupItem.widget()

                    groupName = widget.labelName
                    groupWidgetName = groupWidget.labelName
                    groupWidgetColor = groupWidget.saveColorJson
                    groupWidgetObjects = groupWidget.stored_selection

                    groupDict["Group"] = groupName
                    groupDict["Name"] = groupWidgetName
                    groupDict["Color"] = groupWidgetColor
                    groupDict["Objects"] = groupWidgetObjects 

                    self.data["sets"].append(groupDict)

                    
        # saving dictionaries to json file
        if not fileName:
            retval = cmds.fileDialog2(dialogStyle = 2, fm = 0)
            if retval:
                file, ext = os.path.splitext(retval[0])
                if ext != "*.json":
                    fileName = file + ".json"
                else:
                    fileName = retval[0]
        
        print(fileName)

        fileOut = open(fileName, "w")
        json.dump(self.data, fileOut, indent = 2)
        fileOut.close()         

        sys.stdout.write("Your set has been saved")
        
    
    
    #### drag and drop functions ###

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        name = event.mimeData().getSomeText()
        objList = event.mimeData().getSomeSetList()
        parentLayout = event.mimeData().getSomeLayout()
        palette = event.mimeData().getSomeColor()
        eye = event.mimeData().getSomeEye()
        switch = event.mimeData().getSomeSwitch() 
        widget = ns.CustomSet(labelName = name, color = palette)
    
        widget.stored_selection = objList
        widget.deleteScrollPressed.connect(self.delete_selected_widget)
        widget.visButton.setIcon(eye)

        if switch == 2:
            widget.visButton.setChecked(True)
            widget.vis_Switch_parameter_2 = 2

        if switch == 1:
            widget.vis_Switch_parameter_2 = 1      

        # functions #
        self.addObjects(widget = widget, labelName = name, layout = parentLayout)

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def addObjects(self, widget = None, labelName = None, layout = None):
        
        if self.scroll_layout.count() > 0:
            for i in range(0, self.scroll_layout.count()):
                item = self.scroll_layout.itemAt(i)
                itemWidget = item.widget()
                if itemWidget.labelName == labelName:
                    return
        
        self.scroll_layout.addWidget(widget)

        if layout.count() > 0:
            for i in range(0, layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                pw = layout.parentWidget()
                height = pw.height()
                if widget.labelName == labelName:
                    widget.deleteLater()
                    
                    if hasattr(pw, "DropSize"):
                        pw.setFixedHeight(height - 45)
                        self.repaint()
                        self.update()           
    
# deleting GUI interface before opening new
def deleteGUI(control):

    if cmds.workspaceControl(control, q = True, exists = True):
        cmds.workspaceControl(control, e = True, close = True)

        cmds.deleteUI(control, control = True) 
        sys.stdout.write("I Select has been deleted and reopened")       

    else:

        sys.stdout.write("I select has been opened")

# running gui function
def runGUI():

    deleteGUI("GUI_objectWorkspaceControl")

    dialog = I_Select_GUI()
    dialog.show(dockable = True, floating = True)
    
    cmds.workspaceControl("GUI_objectWorkspaceControl", e = True, wp = 320) 
    dialog.raise_() 
       
             
        