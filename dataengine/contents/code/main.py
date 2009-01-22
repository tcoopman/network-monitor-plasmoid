# -*- coding: utf-8 -*-
#

from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4 import plasmascript

import kotnetlogin

class PyKotnetEngine(plasmascript.DataEngine):
    def __init__(self,parent,args=None):
        plasmascript.DataEngine.__init__(self,parent)

    def init(self):
        #update mostly once in a minutes = 1000msec * 60
        self.setMinimumPollingInterval(1000 * 60)
        #update default once in 10 minutes
        self.setPollingInterval(1000 * 60 * 10)

    def sources(self):
        sources = ["Local"]
        sources.extend(KSystemTimeZones.zones().keys())
        return sources

    # request a new DataEngine
    def sourceRequestEvent(self, name):
        #create an empty source
        self.setData(name, self.Data())
        self.reader = KotnetReader()
    
        return self.updateSourceEvent(name)

    def updateSourceEvent(self, name):
        #TODO implement
        #info = self.reader.login(username, password)
        #set data to info
        return True
    

def CreateDataEngine(parent):
    return PyKotnetEngine(parent)