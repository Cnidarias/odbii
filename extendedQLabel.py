from PyQt4.QtGui import *
from PyQt4.QtCore import *


class ExtendedQLabel( QLabel ):
    def __init__( self, parent ):
        QLabel.__init__(self, parent)
        self.data = ""

    def setData( self, data ):
        self.data = data

    def getData( self ):
        return self.data 

    def mouseReleaseEvent( self, ev ):       
        self.emit( SIGNAL('clicked( QObject )'), self )

    def wheelEvent( self, ev ):
        self.emit( SIGNAL('scroll(int)'), ev.delta() )
