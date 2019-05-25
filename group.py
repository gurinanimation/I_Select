from Qt import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
import os
import json
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQWidgetBaseMixin, MayaQDockWidget

from Qt.QtWidgets import QMainWindow, QMenu
from Qt.QtGui import QColor

import logging
import new_set as ns

ROOT  = str(os.path.dirname(__file__))

class DropGroup(QtWidgets.QWidget):
    def __init__(self, DropSize = 45, label = None):
        super(DropGroup,self).__init__()
        self.DropSize = DropSize
        ###########################
        self.setFixedHeight(self.DropSize)
        self.setObjectName("Drop_group_obj")
        self.drop_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.drop_layout) 
        
        self.bgcolor = 85
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(self.bgcolor,self.bgcolor,self.bgcolor))
        self.setPalette(self.p)

        ### drag and Drop ###
        self.setAcceptDrops(True)

    #### drag and drop functions ###
    def addObjects(self, widget = None, labelName = None, layout = None):
        
        if self.drop_layout.count() > 0:
            for i in range(0, self.drop_layout.count()):
                item = self.drop_layout.itemAt(i)
                itemWidget = item.widget()
                if itemWidget.labelName == labelName:
                    return
        
        self.setFixedHeight(self.height() + 45)
        self.drop_layout.addWidget(widget)
        self.repaint()
        self.update()

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
            
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    
    def dropEvent(self, event):
        name = event.mimeData().getSomeText()
        objList = event.mimeData().getSomeSetList()
        parentLayout = event.mimeData().getSomeLayout()
        palette = event.mimeData().getSomeColor() 
        widget = ns.CustomSet(labelName = name, color = palette)
    
        widget.stored_selection = objList
        widget.deleteScrollPressed.connect(self.delete_selected_widget)

        # functions #
        self.addObjects(widget = widget, labelName = name, layout = parentLayout)
        

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def delete_selected_widget(self, labelName = None):
        if not labelName:
            return

        elif self.drop_layout.count() > 0:
            for i in range(0, self.drop_layout.count()):
                item = self.drop_layout.itemAt(i)
                itemWidget = item.widget()
                if itemWidget.labelName == labelName:
                    itemWidget.deleteLater()
                    self.setFixedHeight(self.height() - 45)

                     
class Label(QtWidgets.QWidget):
    
    emitChangeLabel = QtCore.Signal(str)
    
    def __init__(self, name = None):

        super(Label, self).__init__()
        self.name = name
        
        self.setFixedHeight(16)                       # setting label class sizes
        self.setObjectName("Label_class")               # setting object name 
        
        # label
        self.labelLayout = QtWidgets.QHBoxLayout()      # setting layout for label widget
        self.labelLayout.setContentsMargins(0,0,0,0)    # setting contents margins for layout
        self.setLayout(self.labelLayout)
        
        self.setLabel = QtWidgets.QLabel()            # setting label for set
        self.labelLayout.addWidget(self.setLabel)     # adding setLabel to main layout

        self.setLabel.setText(self.name)

        self.changeLabel = QtWidgets.QLineEdit()          # setting hidden line edit to change set name 
        self.labelLayout.addWidget(self.changeLabel)       # adding line adit to main layout 
        self.changeLabel.hide()                           # hide line edit
        self.changeLabel.textChanged.connect(self.changeText)  # connecting to function to change text
        self.changeLabel.returnPressed.connect(self.setLabel_visibility) # connecting to function line edit visibility
        self.changeLabel.editingFinished.connect(self.changeFocus) # connecting to change focus function

    def mouseDoubleClickEvent(self, event): # Event to hide label and show line edit
        self.setLabel.hide()
        self.changeLabel.show()
    
    def changeText(self, text):             #function to change text in setLabel
        self.setLabel.setText(text)
        self.name = text     
         
    def setLabel_visibility(self):          # function to change setLabel visibility
        self.setLabel.show()     
        self.changeLabel.hide()
        self.emitChangeLabel.emit(str(self.name))       
    
    def changeFocus(self):                  # change focus function to remove focus from changeLabel line edit
        self.setLabel.setFocus() 


class NewGroup(QtWidgets.QWidget):

    ################################
    ### group for nested sets ######
    ################################
    deletePressed = QtCore.Signal(str) 
    
    def __init__(self, labelName = None):
        super(NewGroup, self).__init__()
        self.labelName = labelName
        self.drop = DropGroup()
        
        ###################################
        # adding main layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setObjectName("New_Group")
        self.setMinimumHeight(30 + self.drop.height())
            
        self.mainLayout.setSpacing(10)
        self.mainLayout.setContentsMargins(1,1,1,1)
        
        # group and layout for label and open/close button
        self.label_group = QtWidgets.QGroupBox()
        self.group_layout = QtWidgets.QHBoxLayout()
        self.group_layout.setContentsMargins(0,0,0,0)

        self.label_group.setLayout(self.group_layout)
        self.label_group.setFixedHeight(25)
        
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
        self.groupName = Label(name = self.labelName)
        self.groupName.emitChangeLabel.connect(self.changeLabelName)
        self.group_layout.addWidget(self.groupName)
        self.font = QtGui.QFont("Arial", 10)
        self.groupName.setFont(self.font)

        ### adding drop group to self.mainLayout  ###
        self.mainLayout.addWidget(self.drop)

        ## connect to functions ##
        self.smallBox.clicked.connect(self.open_close_group)

        self.setAutoFillBackground(True)
      
    ### function to change icon on open close group ###
    def open_close_group(self):
        
        if self.smallBox.isChecked():
            self.smallBox.setIcon(self.closeIcon)
            self.drop.setVisible(False)
            self.setMinimumHeight(45)     
            
        else:
            self.smallBox.setIcon(self.openIcon)
            self.drop.setVisible(True)
            self.setMinimumHeight(45 + self.drop.height())
    
    ### context menu #########################    
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        delButton = contextMenu.addAction("Delete Group")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == delButton:
            self.delete_from_set()

    def delete_from_set(self):
        self.deletePressed.emit(self.labelName)

    ### function to change label name ###
    
    @QtCore.Slot(str)
    def changeLabelName(self, text):
        self.labelName = text

    







