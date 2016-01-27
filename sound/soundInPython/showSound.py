import sys
from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qtc
import subprocess

import matplotlib.pyplot as plt
from scipy.fftpack import fft

from sfft import getHZfromSample

import soundProcessor

class CarColorChanger(qt.QWidget):
    
    def __init__(self , data ):
        super(CarColorChanger, self).__init__()
        self.data = data

        self.mkHz = getHZfromSample()

        self.task = soundProcessor.getSound( data )
        self.task.daemon = True
        self.task.start()

        self.max = 0
        self.min = 0

        self.MIN = -800
        self.MAX = 200


        self.freqRatioBase = 1500

        
        self.changingColor0 = [255, 0, 0]
        self.changingColor1 = [255, 0, 0]
        self.changingColor2 = [255, 0, 0]
        self.changingColor3 = [255, 0, 0]
        self.changingColor4 = [255, 0, 0]
        self.increasingIndex = 0
        self.increasing = "G"
        self.increasingSequence = "GrBgRb"
        self.increasingRate = 80
        self.timerChange = 0
        self.timerAmount = 10
        self.counter = 0

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
          #print "MAX: " + str( self.max ) + "\nMIN: " + str( self.min ) + "\n"
          pass


      #self.numberIsColorMethod()
      #self.shadesOfColor( ( 0, 255, 0 ) )
      self.shadesOfColorCircle()
      #self.blackWhiteFreq()

    

    def blackWhiteFreq( self ):
      freq = self.mkHz.getHz( self.data['all'], 44100 )
      ratio =  freq / 2500.0
      r = 255 * ratio
      g = 255 * ratio
      b = 255 * ratio

      self.changeWidgetColor( self.wid0, r, g, b )
      self.changeWidgetColor( self.wid2, r, g, b )

      self.changeWidgetColor( self.wid1, r, g, b )
      self.changeWidgetColor( self.wid3, r, g, b )

      self.changeWidgetColor( self.wid4, r, g, b )


      


    def shadesOfColor( self, color, widget = None, side = None ):
      freqL = self.mkHz.getHz( self.data['leftAll'], 44100 )
      freqR = self.mkHz.getHz( self.data['rightAll'], 44100 )

      r = color[0]
      g = color[1]
      b = color[2]

      #ratioL = float( ( self.data['left'] - self.MIN ) / float(self.MAX - self.MIN) )
      ratioL = float( freqL / float( self.freqRatioBase ) )
      if ratioL < 0: ratioL = 0
      if ratioL > 1: ratioL = 1

      leftR = ratioL * r
      leftG = ratioL * g
      leftB = ratioL * b

      #ratioR = float( ( self.data['right'] - self.MIN ) / float(self.MAX - self.MIN) )
      ratioR = float( freqR / float( self.freqRatioBase ) )
      if ratioR < 0: ratioR = 0
      if ratioR > 1: ratioR = 1
      
      rightR = ratioR * r
      rightG = ratioR * g
      rightB = ratioR * b


      leftR = self.clamp( 0, leftR, 255 )
      leftG = self.clamp( 0, leftG, 255 )
      leftB = self.clamp( 0, leftB, 255 )

      rightR = self.clamp( 0, rightR, 255 )
      rightG = self.clamp( 0, rightG, 255 )
      rightB = self.clamp( 0, rightB, 255 )
      
      
      if widget == None:
        self.changeWidgetColor( self.wid0, leftR, leftG, leftB )
        self.changeWidgetColor( self.wid2, leftR, leftG, leftB )

        self.changeWidgetColor( self.wid1, rightR, rightG, rightB )
        self.changeWidgetColor( self.wid3, rightR, rightG, rightB )

        self.changeWidgetColor( self.wid4, (leftR + rightR)/2, (leftG + rightG)/2, (leftB + rightB)/2 )

      else:
        if side == "left": self.changeWidgetColor( widget, leftR, leftG, leftB )
        elif side == "right" : self.changeWidgetColor( widget, rightR, rightG, rightB )
        elif side == "center" : self.changeWidgetColor( widget, (leftR + rightR)/2, (leftG + rightG)/2, (leftB + rightB)/2 )


    def shadesOfColorCircle( self ):
      self.timerChange += 1
      if self.timerChange >= self.timerAmount:
        self.timerChange = 0

        self.changingColor1[0] = self.changingColor2[0]
        self.changingColor1[1] = self.changingColor2[1]
        self.changingColor1[2] = self.changingColor2[2]

        self.changingColor2[0] = self.changingColor3[0]
        self.changingColor2[1] = self.changingColor3[1]
        self.changingColor2[2] = self.changingColor3[2]

        self.changingColor3[0] = self.changingColor4[0]
        self.changingColor3[1] = self.changingColor4[1]
        self.changingColor3[2] = self.changingColor4[2]

        self.changingColor4[0] = self.changingColor0[0]
        self.changingColor4[1] = self.changingColor0[1]
        self.changingColor4[2] = self.changingColor0[2]

        if self.increasing == "R": self.changingColor0[0] += self.increasingRate
        elif self.increasing == "r": self.changingColor0[0] -= self.increasingRate
        elif self.increasing == "G": self.changingColor0[1] += self.increasingRate
        elif self.increasing == "g": self.changingColor0[1] -= self.increasingRate
        elif self.increasing == "B": self.changingColor0[2] += self.increasingRate
        elif self.increasing == "b": self.changingColor0[2] -= self.increasingRate


        self.shadesOfColor( self.changingColor0, self.wid0, "left" )
        self.shadesOfColor( self.changingColor1, self.wid1, "right" )
        self.shadesOfColor( self.changingColor2, self.wid3, "right" )
        self.shadesOfColor( self.changingColor3, self.wid4, "center" )
        self.shadesOfColor( self.changingColor4, self.wid2, "left" )

        self.counter += self.increasingRate

        if self.counter >= 255:
          self.counter = 0
          self.increasingIndex = ( self.increasingIndex + 1 ) % len( self.increasingSequence )
          self.increasing = self.increasingSequence[ self.increasingIndex ]
          self.changingColor0[0] = self.clamp( 0, self.changingColor0[0], 255 )
          self.changingColor0[1] = self.clamp( 0, self.changingColor0[1], 255 )
          self.changingColor0[2] = self.clamp( 0, self.changingColor0[2], 255 )
      else:
        self.shadesOfColor( self.changingColor0, self.wid0, "left" )
        self.shadesOfColor( self.changingColor1, self.wid1, "right" )
        self.shadesOfColor( self.changingColor2, self.wid3, "right" )
        self.shadesOfColor( self.changingColor3, self.wid4, "center" )
        self.shadesOfColor( self.changingColor4, self.wid2, "left" )

    def clamp( self, minimum, x, maximum ):
        return max( minimum, min( x, maximum ) )


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
