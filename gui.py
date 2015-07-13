import os
import subprocess


kw = subprocess.Popen( ["python", "kw1281Audi.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False )


print kw

while True:
  print kw.pid
  print "RPM", os.getenv('pythonRPM', "n/a")
  print "KMH", os.getenv('pythonKMH', "n/a")
