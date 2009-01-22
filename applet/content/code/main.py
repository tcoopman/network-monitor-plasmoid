# -*- coding: utf-8 -*-
# Copyright stuff
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

class KotnetLoginApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        
        plasmascript.Applet.__init__(self,parent)

    def init(self):

        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.Square)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        label = Plasma.Label(self.applet)
        label.setText("Hello world!")
        self.layout.addItem(label)
        self.resize(125,125)
        
        
    def connectToEngine(self):
        self.engine = self.dataEngine("Python Kotnet engine")
        #TODO
        
    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        #TODO

def CreateApplet(parent):
    return KotnetLoginApplet(parent)