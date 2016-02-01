import sys
from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qtc
import subprocess

from sfft import getHZfromSample
from base64 import b64decode

import soundProcessor


class getRGB():
  def __init__( self ):
    self.mkHz = getHZfromSample()
    
    
    self.max = 0
    self.min = 0
    
    self.MIN = -800
    self.MAX = 200
    
    
    self.freqRatioBase = 350
    
    
    self.changingColor0 = [255, 0, 0]
    self.changingColor1 = [255, 0, 0]
    self.changingColor2 = [255, 0, 0]
    self.changingColor3 = [255, 0, 0]
    self.changingColor4 = [255, 0, 0]
    self.increasingIndex = 0
    self.increasing = "G"
    self.increasingSequence = "GrBgRb"
    self.increasingRate = 20
    self.timerChange = 0
    self.timerAmount = 100
    self.counter = 0



    self.colors = [
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0]
        ]



  def blackWhiteFreq( self, data ):
    freq = self.mkHz.getHz( data['all'], 44100 )
    ratio =  freq / 2500.0
    r = 255 * ratio
    g = 255 * ratio
    b = 255 * ratio

    for strip in self.colors:
      strip[0] = r
      strip[1] = g
      strip[2] = b
    return self.colors
    

  def colorsForFreq( self, data ):
    freqL = self.mkHz.getHz( data['leftAll'], 44100 )
    freqR = self.mkHz.getHz( data['rightAll'], 44100 )
    pass


  def shadesOfColor( self, color, data, colorIndex = -1, noSound = False ):
    if not noSound:
      freqL = self.mkHz.getHz( b64decode( data['leftAll'] ), 44100 )
      freqR = self.mkHz.getHz( b64decode( data['rightAll'] ), 44100 )

      ratioL = float( freqL / float( self.freqRatioBase ) )
      if ratioL < 0: ratioL = 0
      if ratioL > 1: ratioL = 1

      ratioR = float( freqR / float( self.freqRatioBase ) )
      if ratioR < 0: ratioR = 0
      if ratioR > 1: ratioR = 1

    else:
      ratioL = 1
      ratioR = 1


    r = color[0]
    g = color[1]
    b = color[2]

    
    leftR = ratioL * r
    leftG = ratioL * g
    leftB = ratioL * b

    rightR = ratioR * r
    rightG = ratioR * g
    rightB = ratioR * b


    leftR = self.clamp( 0, leftR, 255 )
    leftG = self.clamp( 0, leftG, 255 )
    leftB = self.clamp( 0, leftB, 255 )

    rightR = self.clamp( 0, rightR, 255 )
    rightG = self.clamp( 0, rightG, 255 )
    rightB = self.clamp( 0, rightB, 255 )


    if colorIndex < 0:
      self.setColorFromStereo( leftR, leftG, leftB, rightR, rightG, rightB )
      return self.colors
    else:
      self.setSpecificColor( leftR, leftG, leftB, rightR, rightG, rightB, colorIndex )



  def setSpecificColor ( self, lR, lG, lB, rR, rG, rB, index ):
    if index == 4:
      self.colors[index][0] = (lR + rR) / 2.0
      self.colors[index][1] = (lG + rG) / 2.0
      self.colors[index][2] = (lB + rB) / 2.0
    elif index % 2 == 0:
      self.colors[index][0] = lR
      self.colors[index][1] = lG
      self.colors[index][2] = lB
    else:
      self.colors[index][0] = rR
      self.colors[index][1] = rG
      self.colors[index][2] = rB




  def setColorFromStereo( self, lR, lG, lB, rR, rG, rB ):
    self.colors[0][0] = lR
    self.colors[0][1] = lG
    self.colors[0][2] = lB

    self.colors[1][0] = rR
    self.colors[1][1] = rG
    self.colors[1][2] = rB

    self.colors[2][0] = lR
    self.colors[2][1] = lG
    self.colors[2][2] = lB

    self.colors[3][0] = rR
    self.colors[3][1] = rG
    self.colors[3][2] = rB

    self.colors[4][0] = (lR + rR) / 2.0 
    self.colors[4][1] = (lG + rG) / 2.0  
    self.colors[4][2] = (lB + rB) / 2.0 

    
    

  def shadesOfColorCircle( self, data, noSound = False ):
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


      self.shadesOfColor( self.changingColor0, data, 0, noSound )
      self.shadesOfColor( self.changingColor1, data, 1, noSound )
      self.shadesOfColor( self.changingColor2, data, 3, noSound )
      self.shadesOfColor( self.changingColor3, data, 4, noSound )
      self.shadesOfColor( self.changingColor4, data, 2, noSound )

      self.counter += self.increasingRate

      if self.counter >= 255:
        self.counter = 0
        self.increasingIndex = ( self.increasingIndex + 1 ) % len( self.increasingSequence )
        self.increasing = self.increasingSequence[ self.increasingIndex ]
        self.changingColor0[0] = self.clamp( 0, self.changingColor0[0], 255 )
        self.changingColor0[1] = self.clamp( 0, self.changingColor0[1], 255 )
        self.changingColor0[2] = self.clamp( 0, self.changingColor0[2], 255 )
    else:
      self.shadesOfColor( self.changingColor0, data, 0, noSound )
      self.shadesOfColor( self.changingColor1, data, 1, noSound )
      self.shadesOfColor( self.changingColor2, data, 3, noSound )
      self.shadesOfColor( self.changingColor3, data, 4, noSound )
      self.shadesOfColor( self.changingColor4, data, 2, noSound )


    return self.colors



  def clamp( self, minimum, x, maximum ):
      return max( minimum, min( x, maximum ) )





class CarColorChanger(qt.QWidget):
    
    def __init__(self , data ):
        super(CarColorChanger, self).__init__()
        self.data = data

        self.task = soundProcessor.getSound( data )
        self.task.daemon = True
        self.task.start()

        self.initUI()
        self.colorMaker = getRGB()
        self.colors = None
        
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

      self.color = self.colorMaker.shadesOfColorCircle( self.data, True )

      self.changeWidgetColor( self.wid0, self.color[0][0], self.color[0][1], self.color[0][2] )
      self.changeWidgetColor( self.wid1, self.color[1][0], self.color[1][1], self.color[1][2] )

      self.changeWidgetColor( self.wid2, self.color[2][0], self.color[2][1], self.color[2][2] )
      self.changeWidgetColor( self.wid3, self.color[3][0], self.color[3][1], self.color[3][2] )

      self.changeWidgetColor( self.wid4, self.color[4][0], self.color[4][1], self.color[4][2] )

    

    


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
