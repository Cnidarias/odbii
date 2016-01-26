import sys
from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qtc
import subprocess

import soundProcessor


class CarColorChanger(qt.QWidget):
    
    def __init__(self , data ):
        super(CarColorChanger, self).__init__()
        self.data = data

        self.task = soundProcessor.getSound( data )
        self.task.daemon = True
        self.task.start()

        self.max = 0
        self.min = 0

        self.MIN = -250
        self.MAX = 250
        
        self.initUI()
        
    def initUI(self):

        
        grid = qt.QGridLayout()
        self.setLayout(grid)
 
        self.wid0 = qt.QWidget()
        self.wid0.setFixedSize( 200, 200 )
        self.changeWidgetColor( self.wid0, 0, 0, 0 )
        grid.addWidget( self.wid0, 0,0 )
        
        self.wid1 = qt.QWidget()
        self.wid1.setFixedSize( 200, 200 )
        self.changeWidgetColor( self.wid1, 255, 0, 0 )
        grid.addWidget( self.wid1, 0,1 )
      
        self.wid2 = qt.QWidget()
        self.wid2.setFixedSize( 200, 200 )
        self.changeWidgetColor( self.wid2, 0, 255, 0 )
        grid.addWidget( self.wid2, 1,0 )
        
        self.wid3 = qt.QWidget()
        self.wid3.setFixedSize( 200, 200 )
        self.changeWidgetColor( self.wid3, 0, 0, 255 )
        grid.addWidget( self.wid3, 1,1 )


        self.wid4 = qt.QWidget()
        self.wid4.setFixedSize( 400, 100 )
        self.changeWidgetColor( self.wid4, 0, 0, 255 )
        grid.addWidget( self.wid4, 2,0, 2, 2, qtc.Qt.AlignCenter )
            
        self.move(300, 150)
        self.setWindowTitle('Car')
        self.show()

        self.timer = qtc.QTimer( self )
        self.timer.setInterval( 10 )
        self.timer.timeout.connect( self.custUpdate )
        self.timer.start()
 

    def custUpdate( self ):
      if self.data['left'] > self.max: self.max = self.data['left']  
      if self.data['left'] < self.min: self.min = self.data['left']  

      if self.data['left'] == self.min or self.data['left'] == self.max:
          print "MAX: " + str( self.max ) + "\nMIN: " + str( self.min ) + "\n"
      self.numberIsColorMethod()
      #self.shadesOfColor( 0, 255, 0 )

    

    def rangeOfColors( self ):
      pass
      


    def shadesOfColor( self, r, g, b ):
      ratioL = float( ( self.data['left'] - self.MIN ) / float(self.MAX - self.MIN) )
      if ratioL < 0: ratioL = 0
      if ratioL > 255: ratioL = 255

      leftR = ratioL * r
      leftG = ratioL * g
      leftB = ratioL * b

      ratioR = float( ( self.data['right'] - self.MIN ) / float(self.MAX - self.MIN) )
      if ratioR < 0: ratioR = 0
      if ratioR > 255: ratioR = 255
      
      rightR = ratioR * r
      rightG = ratioR * g
      rightB = ratioR * b
      
      
      self.changeWidgetColor( self.wid0, leftR, leftG, leftB )
      self.changeWidgetColor( self.wid2, leftR, leftG, leftB )

      self.changeWidgetColor( self.wid1, rightR, rightG, rightB )
      self.changeWidgetColor( self.wid3, rightR, rightG, rightB )

      self.changeWidgetColor( self.wid4, (leftR + rightR)/2, (leftG + rightG)/2, (leftB + rightB)/2 )




    def numberIsColorMethod( self ):
      leftR = ( self.data['left'] >> 0 ) & 0xff
      leftG = ( self.data['left'] >> 5 ) & 0xff
      leftB = ( self.data['left'] >> 11 ) & 0xff

      rightR = ( self.data['right'] >> 0 ) & 0xff
      rightG = ( self.data['right'] >> 5 ) & 0xff
      rightB = ( self.data['right'] >> 11 ) & 0xff


      self.changeWidgetColor( self.wid0, leftR, leftG, leftB )
      self.changeWidgetColor( self.wid2, leftR, leftG, leftB )

      self.changeWidgetColor( self.wid1, rightR, rightG, rightB )
      self.changeWidgetColor( self.wid3, rightR, rightG, rightB )

      self.changeWidgetColor( self.wid4, (leftR + rightR)/2, (leftG + rightG)/2, (leftB + rightB)/2 )




    def changeWidgetColor( self, widget, r, g, b ):
      widget.setAutoFillBackground( True )
      p = widget.palette()
      p.setColor( widget.backgroundRole(), qt.QColor( r, g, b ) )
      widget.setPalette( p )
        
def main( data ):
    app = qt.QApplication(sys.argv)
    ex = CarColorChanger( data )
    sys.exit(app.exec_())

if __name__ == '__main__':
    data = { 'left' : 0, 'right' : 0 }
    main( data )
