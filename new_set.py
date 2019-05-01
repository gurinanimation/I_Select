from Qt import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
import os
import json
from Qt.QtWidgets import QMainWindow, QMenu
from Qt.QtGui import QColor
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQWidgetBaseMixin, MayaQDockWidget
import logging

ROOT = str(os.path.dirname(__file__))


class MyMIME(QtCore.QMimeData):
    ### this class keeps all the data transfered via drag and drop ###
    def __init__(self):
        super(MyMIME, self).__init__()
        
    def setSomeText(self, text = None):
        self.someText = text
    
    def getSomeText(self):
        return self.someText 

    def setSomeSetList(self, setList = None):
        self.someSetList = setList

    def getSomeSetList(self):
        return self.someSetList       


class Label(QtWidgets.QWidget):
    # this class keeps label name for the set
    emitChangeLabel = QtCore.Signal(str)
    
    def __init__(self, name = None):

        super(Label, self).__init__()
        self.internalName = name
        
        self.setMinimumWidth(100)                       # setting label class sizes
        self.setMinimumHeight(16)
        self.setObjectName("Label_class")               # setting object name 
        
        self.labelLayout = QtWidgets.QHBoxLayout()      # setting layout for label widget
        self.labelLayout.setContentsMargins(0,0,0,0)    # setting contents margins for layout
        self.setLayout(self.labelLayout)
        
        self.setLabel = QtWidgets.QLabel()            # setting label for set
        self.labelLayout.addWidget(self.setLabel)     # adding setLabel to main layout
        self.font = QtGui.QFont("Arial", 10)          # setting font for label
        self.setLabel.setFont(self.font)              # assigning this font to label
        self.setLabel.setText(self.internalName)

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
        self.internalName = text       
    
    def setLabel_visibility(self):          # function to change setLabel visibility
        self.setLabel.show()     
        self.changeLabel.hide()
        print(self.internalName)       
        self.emitChangeLabel.emit(str(self.internalName)) 
    
    def changeFocus(self):                  # change focus function to remove focus from changeLabel line edit
        self.changeLabel.clearFocus()
        
    
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
        self.setObjectName("Color_cube") 

    def mouseDoubleClickEvent(self, event):    # double click to change color on color cube
        self.color = QtWidgets.QColorDialog.getColor()
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(self.color.red(), self.color.green(), self.color.blue()))
        self.setPalette(self.p)    


class CustomSet(QtWidgets.QWidget):

    ### custom selection set ###
    deleteScrollPressed = QtCore.Signal(str)

    def __init__(self, labelName = None):
        super (CustomSet, self).__init__()
        
        self.labelName = labelName

        self.setMinimumWidth(310)                 # size for custom widget
        self.setMinimumHeight(45)
        self.setMaximumHeight(45)
        self.setObjectName("Custom_set_widget")    # object name for custom widget
        self.mainLayout = QtWidgets.QHBoxLayout()  # layout for custom widget
        self.setLayout(self.mainLayout)            # setting mainLayout as layout for widget

        self.visButton = QtWidgets.QPushButton()     # visibility "Eye" button
        self.visButton.setFixedSize(16,16)         # visibility button size 
        self.mainLayout.addWidget(self.visButton)  # adding visibility button to mainLayout
        self.visButton.setFlat(True)

        self.eyeicon_1 = QtGui.QIcon(os.path.join(ROOT, "icons", "vis.svg"))
        self.eyeicon_2 = QtGui.QIcon(os.path.join(ROOT, "icons", "invis.svg"))
        self.visButton.setIcon(self.eyeicon_1)
        
        
        self.visButton.setStyleSheet("QPushButton:checked{background-color: transparent; color: black; border: black 2px; }"
                                    "QPushButton:pressed{background-color: transparent; color: black; border: black 2px; }")                      
        
        self.visButton.setIconSize(QtCore.QSize(16,16))  # icon size for visibility button
        self.visButton.toggle()
        self.visButton.setCheckable(True)
        
        self.visButton.clicked.connect(self.hideLayer)

        self.colorSwatch = ColorCube()              # Adding color cube class to main layout 
        self.mainLayout.addWidget(self.colorSwatch)

        self.label = Label(name = self.labelName)                        # adding label class to mainLayout
        self.label.emitChangeLabel.connect(self.changeLabelName)
        self.mainLayout.addWidget(self.label)


        self.selButton = QtWidgets.QPushButton("Select")  # Select button
        self.mainLayout.addWidget(self.selButton)         # Adding select button to mainLayout 
        self.selButton.setMinimumHeight(30)               # Select button size
        self.selButton.setMaximumHeight(30)
        self.selButton.setMinimumWidth(50)
        self.selButton.setMaximumWidth(50)
        self.selButton.clicked.connect(self.selection_function)

        #### list for keeping objects in set ####
        self.stored_selection = []
    
    ### changing mainLable ###
    @QtCore.Slot(str)
    def changeLabelName(self, text):
        self.labelName = text
        print("New label name is: " + self.labelName)   
    
    ### function to hide/open layers eye
    def hideLayer(self):
        self.shapes = []
        if self.visButton.isChecked():
            self.visButton.setIcon(self.eyeicon_2)
            for i in self.stored_selection:
                cmds.select(i)
                self.shapes.extend(cmds.listRelatives(c = True, s = True))
                for i in self.shapes:
                    cmds.setAttr("%s.visibility" % i, 0)       
        else:
            self.visButton.setIcon(self.eyeicon_1)
            for i in self.stored_selection:
                cmds.select(i)
                self.shapes.extend(cmds.listRelatives(c = True, s = True))
                for i in self.shapes:
                    cmds.setAttr("%s.visibility" % i, 1)
        cmds.select(cl = True)             
            
    ### function to add objects to list ###
    def adding_to_set_function(self):
        self.temporary = cmds.ls(sl = True, tr = True, l = True)

        if len(self.stored_selection) > 0:
            for i in range(len(self.temporary)):
                flag = 1    
                for j in range(len(self.stored_selection)):
                    if self.temporary[i] == self.stored_selection[j]:
                        logging.info("{} already exists".format(self.temporary[i]))
                        flag = 0   
                if flag == 1:
                    self.stored_selection.append(self.temporary[i])        
                
        else:
            self.stored_selection.extend(self.temporary)               
                        
    ### function to select objects in set ###
    def selection_function(self):
        if len(self.stored_selection):
            cmds.select(self.stored_selection)
        else:
            print ("Nothing to select")
            logging.info("Nothing to select")

        print(self.stored_selection) 
    ### function to delete selected object from set ###
    def delete_objects_from_set(self):
        self.del_selection = cmds.ls(sl = True, tr = True, l = True)

        if len(self.stored_selection) > 0:
            for i in range(len(self.del_selection)):
                flag = 1    
                for j in range(len(self.stored_selection)):
                    if self.del_selection[i] == self.stored_selection[j]:
                        flag = 0   
                if flag == 0:
                    self.stored_selection.remove(self.del_selection[i])

    ### function to delete SET itself from scroll_layout ###
    def delete_from_scroll(self):
        self.deleteScrollPressed.emit(self.labelName)                



    ### context menu ###      
    def contextMenuEvent(self, event):      # creating right click context menu on selection set
     
        contextMenu = QMenu(self)           # context menu                  

        addAct = contextMenu.addAction("Add Selected")        
        removeAct = contextMenu.addAction("Remove Selected")
        delAct = contextMenu.addAction("Delete Set")

        action = contextMenu.exec_(self.mapToGlobal(event.pos())) # menu position where mouse clicked

        if action == addAct:
            self.adding_to_set_function()

        if action == removeAct:
            self.delete_objects_from_set()

        if action == delAct:
            self.delete_from_scroll()

    ###### Drag and Drop section ######
        
    def mouseMoveEvent(self, event):
        
        if event.buttons() != QtCore.Qt.LeftButton:
            return
        
        mimeData = MyMIME()                        # setting MimeData
        mimeData.setSomeText(text = self.labelName)
        mimeData.setSomeSetList(setList = self.stored_selection)
        
        # below makes the pixmap half transparent
        pixmap = QtGui.QPixmap.grabWidget(self)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()
    
        # make a QDrag
        drag = QtGui.QDrag(self)
        # put our MimeData
        drag.setMimeData(mimeData)
        # set its Pixmap
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(event.pos())
    
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.MoveAction)
        










