# -*- coding: utf-8 -*-

import re
from mechanize import Browser

username="USER"
password="PASSWORD"

br = Browser()
br.open("http://netlogin.kuleuven.be/")
br.select_form(name="wayf")
br.submit()
br.select_form(name="netlogin")
br[br.form._pairs()[2][0]]=username
br[br.form._pairs()[3][0]]=password
result = br.submit()
lines = [k for k in result.readlines()]

downloadRe = re.compile("[\w]*download = (\d*) of (\d*)[\w]*")
uploadRe = re.compile("[\w]*upload = (\d*) of (\d*)[\w]*")

downUpRe = re.compile ("[\w]*[download|upload] = (\d*) of (\d*)[\w]*")
revlines = [k for k in lines if downUpRe.search(k)]
downResults = downloadRe.split(revlines[0])
upResults = uploadRe.split(revlines[1])

def prettyPrint(results, updown):
  avail = float(results[1])
  total = float(results[2])
  availMb = avail/1024/1024
  totalMb = total/1024/1024
  percentage = avail/total*100
  print("You have still %2.1f%%(%2.2f of %2.2f) left from your %s."%(percentage,availMb,totalMb,updown))

print("login succeeded")
prettyPrint(downResults, "download")
prettyPrint(upResults, "upload")

  
