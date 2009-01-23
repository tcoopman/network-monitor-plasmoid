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
        titleLabel = Plasma.Label(self.applet)
        titleLabel.setText("This is kotnet!")
        downloadLabel = Plasma.Label(self.applet)
        downloadLabel.setText("initial download")
        self.layout.addItem(titleLabel)
        self.layout.addItem(downloadLabel)
        self.resize(125,125)
        #self.connectToEngine()
        
        
    def connectToEngine(self):
        print "connecting"
        self.engine = self.dataEngine("plasma-dataengine-pytime")
        print "after getting engine"
        self.timeEngine.connectSource("Local", self, 6000, Plasma.AlignToMinute)
        #print "connected"
        
    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        #print "updated"
        #print data
        self.update()
        #print "na self.update()"
        #self.time = data[QString("Time")].toTime()
        
        #if self.time.minute() == self.lastTimeSeen.minute() and \
        #self.time.second() == self.lastTimeSeen.second():
            # avoid unnecessary repaints
         #   return
            
          #  self.lastTimeSeen = self.time
           # self.update()

def CreateApplet(parent):
    return KotnetLoginApplet(parent)