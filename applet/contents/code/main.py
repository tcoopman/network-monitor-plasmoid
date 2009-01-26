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
        
        self.count = 0
        
        self.initGui()
        
        Plasma.Theme.defaultTheme().connect(Plasma.Theme.defaultTheme(), SIGNAL("themeChanged()"), self, SLOT("slotThemeChanged()"))
    
        #self.connectToEngine()
        
    def initGui(self):
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        
        downMeter = self._createMeter("download")
        upMeter = self._createMeter("upload")
        self.meters = [downMeter, upMeter]
        for meter in self.meters:
            self.layout.addItem(meter)
        
        self.resize(250,250)
        
    def _createMeter(self, title):
        meter = Plasma.Meter()
        meter.setMeterType(Plasma.Meter.BarMeterHorizontal)
        meter.setLabel(0, title);
        self._setTheme(meter)
        return meter
        
    def _setTheme(self, meter):
        theme = Plasma.Theme.defaultTheme();
        text = theme.color(Plasma.Theme.TextColor)
        background = theme.color(Plasma.Theme.BackgroundColor)
        darkerText = QColor(
        (text.red() + background.red()) / 2, 
        (text.green() + background.green()) / 2,                     (text.blue() + background.blue()) / 2,
        (text.alpha() + background.alpha()) / 2)
        meter.setLabelColor(0, text)
        meter.setLabelColor(1, darkerText)
        meter.setLabelColor(2, darkerText)
        font = theme.font(Plasma.Theme.DefaultFont)
        font.setPointSize(9)
        meter.setLabelFont(0, font)
        font.setPointSizeF(7.5)
        meter.setLabelFont(1, font)
        meter.setLabelFont(2, font)
        meter.setLabel(1, str(self.count))
        self.count +=1
        
    @pyqtSignature("slotThemeChanged()")  
    def themeChanged(self):
        for meter in self.meters:
            self._setTheme(meter)
        
    def connectToEngine(self):
        print "connecting"
        self.engine = self.dataEngine("kotnet-dataengine")
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