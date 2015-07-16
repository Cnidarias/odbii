import os
import sys
import time
import subprocess
from multiprocessing.connection import Listener

from PyQt4 import QtGui as qt
import pyqtgraph as pg


#kw = subprocess.Popen( ["python", "kw1281Audi.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False )
#
#
#
#
#print kw
#
#
#
#address = ( 'localhost', 6000 )
#listener = Listener( address, authkey="kw1281Audipass" )
#conn = listener.accept()
#
#print "connection accepted from", listener.last_accepted
#
#while True:
#    msg = conn.recv()
#
#    print msg
#    if msg == 'close':
#        conn.close()
#
#        kw = subprocess.Popen( ["python", "kw1281Audi.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False )
#        conn = listener.accept()
#
#


def main():
    app = qt.QApplication( [] )
    
    w = qt.QWidget()
    w.resize( 1024, 600 )
    w.setWindowTitle( 'Board Computer' )
    
    button = qt.QPushButton( 'Button' )
    text = qt.QLineEdit( 'Enter Text' )
    listw = qt.QListWidget()
    plot = pg.PlotWidget()
    
    layout = qt.QGridLayout()
    w.setLayout( layout )
    
    layout.addWidget( button, 0, 0 )
    layout.addWidget( text, 1, 0 )
    layout.addWidget( listw, 2, 0 )
    layout.addWidget( plot, 0, 1, 3, 1 )
    
    w.show()
    
    sys.exit( app.exec_() )



if __name__ == '__main__':
    main()
