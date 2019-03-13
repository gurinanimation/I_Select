import maya.cmds as cmds
import os
import json
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQWidgetBaseMixin, MayaQDockWidget
from Qt import QtWidgets, QtCore, QtGui
from Qt.QtWidgets import QMainWindow, QMenu
import logging

import main_GUI as ui

ROOT  = str(os.path.dirname(__file__))


class I_Select(object):
    def __init__(self):

        run_gui = ui.runGUI()






def main():
    
    ### main entry point ###

    app = I_Select()
    





