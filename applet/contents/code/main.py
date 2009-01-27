# -*- coding: utf-8 -*-
# Copyright stuff
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from LoginMonitorConfig import *

class LoginMonitorApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):

        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.Square)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        
        self.dialog = None
        
        self.initGui()
        
        Plasma.Theme.defaultTheme().connect(Plasma.Theme.defaultTheme(), SIGNAL("themeChanged()"), self, SLOT("slotThemeChanged()"))
    
        #doesn't work for now, big crash :-S
        #self.connectToEngine()
        
        #some tests:
        self.meters["download"].setValue(50)
        self.meters["download"].setLabel(2, str(50))
        self.meters["download"].setLabel(1, str(100))
        self.meters["upload"].setValue(24)
        self.meters["upload"].setLabel(2, str(24))
        self.meters["upload"].setLabel(1, str(100))
        
    def initGui(self):
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        self.layout.setContentsMargins(3, 3, 3, 3)
        self.layout.setSpacing(5);
        
        self.meters = {
                "download": self._createMeter("download"), "upload":self._createMeter("upload")
        }
        for meter in self.meters.values():
            self.layout.addItem(meter)
        
        self.resize(250,250)
        
        self.initWallet()
        
        
        #TODO check if the configuration is saved allready
        #if not setConfigurationRequired + write good message
        self.setConfigurationRequired(True, "message")
        
    def _createMeter(self, title):
        meter = Plasma.Meter()
        meter.setMeterType(Plasma.Meter.BarMeterHorizontal)
        meter.setLabel(0, title);
        self._setTheme(meter)
        meter.setLabelAlignment(0, Qt.AlignVCenter | Qt.AlignLeft)
        meter.setLabelAlignment(1, Qt.AlignVCenter | Qt.AlignRight)
        meter.setLabelAlignment(2, Qt.AlignVCenter | Qt.AlignCenter)
        
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
        
    @pyqtSignature("slotThemeChanged()")  
    def themeChanged(self):
        for meter in self.meters.values():
            self._setTheme(meter)
        
    def connectToEngine(self):
        print "connecting"
        self.engine = self.dataEngine("network-monitor-dataengine")
        print "after getting engine"
        self.engine.connectSource("Local", self, 6000, Plasma.AlignToMinute)
        #print "connected"
        
    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        #print "updated"
        #print data
        self.meters["download"].setValue(50)
        self.meters["download"].setLabel(1, str(50))
        self.meters["download"].setLabel(2, str(100))
        self.update()
        #print "na self.update()"
        #self.time = data[QString("Time")].toTime()
        
        #if self.time.minute() == self.lastTimeSeen.minute() and \
        #self.time.second() == self.lastTimeSeen.second():
            # avoid unnecessary repaints
         #   return
            
          #  self.lastTimeSeen = self.time
           # self.update()
           
           
    def showConfigurationInterface(self):
        windowTitle = str(self.applet.name()) + " Settings" #i18nc("@title:window", "%s Settings" % str(self.applet.name()))
                       
        if self.dialog is None:
            self.dialog = KDialog(None)
            self.dialog.setWindowTitle(windowTitle)
                   
            self.ui = LoginMonitorConfig(self.dialog)
            self.dialog.setMainWidget(self.ui)
            
            self.dialog.setButtons(KDialog.ButtonCodes(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel | KDialog.Apply)))
            self.dialog.showButton(KDialog.Apply, False)
            
            self.connect(self.dialog, SIGNAL("applyClicked()"), self, SLOT("configAccepted()"))
            self.connect(self.dialog, SIGNAL("okClicked()"), self, SLOT("configAccepted()"))
            
        self._fillProviders(self.ui.providerComboBox)
        
        self.dialog.show()
        
    def _fillProviders(self, kcombo):
        providers = QStringList()
        providers.append("provider 1")
        providers.append("provider 2")
        kcombo.addItems(providers)
        
    def initWallet(self):
        w = self.view().winId()
        #FIXME possible that self.view() is not valid
        self.wallet = KWallet.Wallet.openWallet(KWallet.Wallet.NetworkWallet(), w, KWallet.Wallet.Asynchronous)
        KWallet.Wallet.connect(self.wallet, SIGNAL("walletOpened(bool)"), self._initWallet)
        
    def _initWallet(self, success):
        if success:
            self.wallet.createFolder("Plasma-NetworkMonitor")
            self.wallet.setFolder("Plasma-NetworkMonitor")
            for i in self.wallet.folderList():
                print i
        
        self.password = QString()
        self.writeWallet()
        self.readWallet()
        print self.password
                    
    def writeWallet(self):
        if self.wallet.isOpen():
            result = self.wallet.writePassword("test", "passwordTest")
            if result == 0:
                print "successfully put password in wallet, removing from config file"
            else:
                print "failed"
                                
    def readWallet(self):
        if self.wallet.isOpen():
            result = self.wallet.readPassword("test", self.password)
            if result == 0:
                print "read password ok"
            else:
                print "could not read password"
        
    @pyqtSignature("configAccepted()")
    def configAccepted(self):
        print "accepted"
        print(self.config())
        cg = self.config()
        cg.writeEntry("provider", self.ui.providerComboBox.currentText())
        cg.writeEntry("name", self.ui.usernameEdit.text())
        cg.writeEntry("password", self.ui.passwordEdit.text())
        cg.writeEntry("updateInterval", QVariant(self.ui.updateIntervalSpinBox.value()))
        
        print cg.readEntry("provider")
        print cg.readEntry("name")
        print cg.readEntry("password")
        #toInt() returns tupple, first the int, second a Bool, True if succeded, False else
        print cg.readEntry("updateInterval", QVariant(0)).toInt()[0]
        
        self.emit(SIGNAL("configNeedsSaving()"))
            
        
        

def CreateApplet(parent):
    return LoginMonitorApplet(parent)