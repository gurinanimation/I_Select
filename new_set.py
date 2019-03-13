from Qt import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
import os
import json
from Qt.QtWidgets import QMainWindow, QMenu
from Qt.QtGui import QColor
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQWidgetBaseMixin, MayaQDockWidget

ROOT  = str(os.path.dirname(__file__))

class Label(QtWidgets.QWidget):
    def __init__(self):

        super(Label, self).__init__()
        
        self.setMinimumWidth(100)                       # setting label class sizes
        self.setMinimumHeight(16)
        self.setObjectName("Label_class")               # setting object name 
        
        self.labelLayout = QtWidgets.QHBoxLayout()      # setting layout for label widget
        self.labelLayout.setContentsMargins(0,0,0,0)    # setting contents margins for layout
        self.setLayout(self.labelLayout)
        
        self.setLabel = QtWidgets.QLabel("New set")  # setting label for set
        self.labelLayout.addWidget(self.setLabel)     # adding setLabel to main layout
        self.font = QtGui.QFont("Arial", 10)         # setting font for label
        self.setLabel.setFont(self.font)             # assigning this font to label

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
         
    def setLabel_visibility(self):          # function to change setLabel visibility
        self.setLabel.show()     
        self.changeLabel.hide()       
    def changeFocus(self):                  # change focus function to remove focus from changeLabel line edit
        self.setLabel.setFocus() 


class ColorCube(QtWidgets.QWidget):

    ### creating color swatch cube ###
    
    def __init__(self):

        super(ColorCube, self).__init__()
        
        self.setFixedSize(16, 16)              # size for color cube
         
        self.bgcolor = 150                     # Setting color swatch cube color 
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(self.bgcolor, self.bgcolor, self.bgcolor))
        self.setPalette(self.p) 

    def mouseDoubleClickEvent(self, event):    # double click to change color on color cube
        self.color = QtWidgets.QColorDialog.getColor()
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(self.color.red(), self.color.green(), self.color.blue()))
        self.setPalette(self.p)    


class CustomSet(QtWidgets.QWidget):

    ### custom selection set ###

    def __init__(self):
        super (CustomSet, self).__init__()

        self.setMinimumWidth(310)                 # size for custom widget
        self.setMinimumHeight(45)
        self.setMaximumHeight(45)
        self.setObjectName("Custom_set_widget")    # object name for custom widget
        self.mainLayout = QtWidgets.QHBoxLayout()  # layout for custom widget
        self.setLayout(self.mainLayout)            # setting mainLayout as layout for widget

        self.visButton = QtWidgets.QPushButton()   # visibility "Eye" button
        self.visButton.setFixedSize(18,18)         # visibility button size 
        self.mainLayout.addWidget(self.visButton)  # adding visibility button to mainLayout

        self.eyeicon_1 = QtGui.QIcon(os.path.join(ROOT, "icons", "vis.svg"))
        self.eyeicon_2 = QtGui.QIcon(os.path.join(ROOT, "icons", "invis.svg"))
        self.visButton.setIcon(self.eyeicon_1) # icon for visibility Button                      
        self.visButton.setIconSize(QtCore.QSize(16,16))  # icon size for visibility button
        self.visButton.setFlat(True)               # setting button flat and transparent
        
        self.visButton.clicked.connect(self.eyeChanged)

        self.colorSwatch = ColorCube()              # Adding color cube class to main layout 
        self.mainLayout.addWidget(self.colorSwatch)

        self.label = Label()                        # adding label class to mainLayout
        self.mainLayout.addWidget(self.label)


        self.selButton = QtWidgets.QPushButton("Select")  # Select button
        self.mainLayout.addWidget(self.selButton)         # Adding select button to mainLayout 
        self.selButton.setMinimumHeight(30)               # Select button size
        self.selButton.setMaximumHeight(30)
        self.selButton.setMinimumWidth(50)
        self.selButton.setMaximumWidth(50)
 
    def eyeChanged():
        if self.visButton.QIcon() == self.eyeicon_1:
            self.visButton.setIcon(self.eyeicon_2)
        elif self.visButton.QIcon() == self.eyeicon_2:
            self.visButton.setIcon(self.eyeicon_1)        
    
    
    def contextMenuEvent(self, event):      # creating right click context menu on selection set
     
        contextMenu = QMenu(self)           # context menu                  

        addAct = contextMenu.addAction("Add Selected")        
        removeAct = contextMenu.addAction("Remove Selected")
        delAct = contextMenu.addAction("Delete Set ")

        action = contextMenu.exec_(self.mapToGlobal(event.pos())) # menu position where mouse clicked       







