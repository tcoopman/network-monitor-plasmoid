# -*- coding: utf-8 -*-
#

from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4 import plasmascript

from kotnetlogin import KotnetReader

class NetworkMonitorEngine(plasmascript.DataEngine):
    def __init__(self,parent,args=None):
        plasmascript.DataEngine.__init__(self,parent)
        self.username = "user"
        self.password = "pass"

    def init(self):
        #update mostly once in a minutes = 1000msec * 60
        self.setMinimumPollingInterval(1000 * 60)
        #update default once in 10 minutes
        self.setPollingInterval(1000 * 60 * 10)

    def sources(self):
        self.sources = []
        return self.sources
        #sources.extend(KSystemTimeZones.zones().keys())
        #return sources
        #pass

    # request a new DataEngine
    def sourceRequestEvent(self, name):
        #create an empty source
        print(name)
        self.sources.append(name)
        self.reader = KotnetReader()
    
        return self.updateSourceEvent(name)

    def updateSourceEvent(self, name):
        #TODO implement
        info = self.reader.login(self.username, self.password)
        #set data to info
        self.setData(name, "downloadAvailable", QVariant(info.download["available"]))
        self.setData(name, "downloadTotal", QVariant(info.download["total"]))
        self.setData(name, "uploadAvailable", QVariant(info.upload["available"]))
        self.setData(name, "uploadTotal", QVariant(info.upload["total"]))
        return True
    

def CreateDataEngine(parent):
    return NetworkMonitorEngine(parent)