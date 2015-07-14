import time
import os
import subprocess
from multiprocessing.connection import Listener


kw = subprocess.Popen( ["python", "kw1281Audi.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False )




print kw



address = ( 'localhost', 6000 )
listener = Listener( address, authkey="kw1281Audipass" )
conn = listener.accept()

print "connection accepted from", listener.last_accepted

while True:
    msg = conn.recv()

    print msg
    if msg == 'close':
        conn.close()

        kw = subprocess.Popen( ["python", "kw1281Audi.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False )
        conn = listener.accept()


listener.close()
