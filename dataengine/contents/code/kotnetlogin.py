# -*- coding: utf-8 -*-

import re
from mechanize import Browser

class KotnetReader:
    def __init__(self):
        self.downloadRe = re.compile("[\w]*download = (\d*) of (\d*)[\w]*")
        self.uploadRe = re.compile("[\w]*upload = (\d*) of (\d*)[\w]*")
        self.downUpRe = re.compile ("[\w]*[download|upload] = (\d*) of (\d*)[\w]*")

    def login(self, username, password):
        html = self._login(username, password)
        info = self._parseAll(html)
        
        return info

    def _login(self, username, password):
        br = Browser()
        br.open("http://netlogin.kuleuven.be/")
        br.select_form(name="wayf")
        br.submit()
        br.select_form(name="netlogin")
        br[br.form._pairs()[2][0]]=username
        br[br.form._pairs()[3][0]]=password
        result = br.submit()
        lines = [k for k in result.readlines()]
        br.close()
        
        return lines

    def _parseAll(self, lines):
        revlines = [k for k in lines if self.downUpRe.search(k)]
        downloadResults = self.downloadRe.split(revlines[0])
        uploadResults = self.uploadRe.split(revlines[1])

        info = KotnetInfo()
        info.download = self._parseSingle(downloadResults)
        info.upload = self._parseSingle(uploadResults)

        return info

    def _parseSingle(self, results):
        available = float(results[1])
        total = float(results[2])
        print available
        print total

        return {"available":available, "total":total}
        
class KotnetInfo:
    def __init__(self):
        pass

    #TODO add extra information to this class, like succesfully logged in and such

  

