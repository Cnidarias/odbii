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
        
        self.initUI()
        
    def initUI(self):

        
        grid = qt.QGridLayout()
        self.setLayout(grid)
 
        self.wid0 = qt.QWidget()
        self.wid0.setFixedSize( 300, 300 )
        self.changeWidgetColor( self.wid0, 0, 0, 0 )
        grid.addWidget( self.wid0, 0,0 )
        
        self.wid1 = qt.QWidget()
        self.wid1.setFixedSize( 300, 300 )
        self.changeWidgetColor( self.wid1, 255, 0, 0 )
        grid.addWidget( self.wid1, 0,1 )
      
        self.wid2 = qt.QWidget()
        self.wid2.setFixedSize( 300, 300 )
        self.changeWidgetColor( self.wid2, 0, 255, 0 )
        grid.addWidget( self.wid2, 1,0 )
        
        self.wid3 = qt.QWidget()
        self.wid3.setFixedSize( 300, 300 )
        self.changeWidgetColor( self.wid3, 0, 0, 255 )
        grid.addWidget( self.wid3, 1,1 )
        print self.data

            
        self.move(300, 150)
        self.setWindowTitle('Car')
        self.show()

        self.timer = qtc.QTimer( self )
        self.timer.setInterval( 10 )
        self.timer.timeout.connect( self.custUpdate )
        self.timer.start()
 

    def custUpdate( self ):
      self.numberIsColorMethod()

    

    def rangeOfColors( self ):
#####     // JavaScript routine to convert a wavelength of light to RGB color 
#####//  by Clint Goss.
#####
#####// the original C# code by Phillip Lave is from:
#####//  http://miguelmoreno.net/sandbox/wavelengthtoRGB/
#####
#####// The Philip Lavid documentation says:
#####//
#####// Determining RGB Color from a wavelength in C#
#####// While working on a software project with Flow Cytometers,
#####//  I had to find the specific color for a specific laser wavelength
#####//  and could really find much online. I decided to write a quick
#####//  app that would accept an integer (wavelength) and returns
#####//  a System.Color object. With a little modification you can have
#####//  it return either of the three RGB values. 
#####// 
#####// To convert a particular wavelength of light into a colour that can
#####//  be displayed on a computer monitor, an algorithm is necessary
#####//  to generate RGB values (the amplitude of Red, Green and Blue
#####//  signals) used by the computer display. The code is based on an
#####//  algorithm from Dan Bruton's Color Science Page.  The conversion
#####//  process from wavelength to RGB values is shown graphically below,
#####//  together with the resulting display of spectrum from 380 to 700 nm.
#####//  The Bruton algorithm is obviously a simplification of a complex process.
#####//   More complex algorithms have been investigated, such as those
#####//  developed by CIE (Commission Internationale Eclairage -
#####//  International Lighting Commission) but none of them produce an
#####//  aesthetically pleasing spectrum! As the coloured depictions of optical
#####//  phenomena depend crucially on the relationship between wavelength
#####//  and colour, more work is required in this area. [Phillip Laven] 
#####// === End of Phillip Laven documentation.
#####
#####// 12/11/2010 Clint Goss
#####//    Converted from C# to JavaScript
#####//
#####//  12/12/2010 Clint Goss
#####//    Substantial updates to close "holes" in the range of wavelengths handled.
#####//    Also adjusted intensity for better renditions.
#####
#####// Take a wavelength in Nanometers in the range 350-780  nm and return the
#####// equivalent RGB color in the format of #RRGGBB where RR, GG, and BB
#####// are in lower-case Hexidecimal.
#####
#####
#####function getColorFromWaveLength (wavelength) {
#####  var Gamma = 1.00;
#####  var IntensityMax = 255;
#####
#####  var Factor;
#####  
#####  // Color values in the range -1 to 1
#####  var Blue;
#####  var Green;
#####  var Red;
#####
#####  if (wavelength >= 350 && wavelength < 440) {
#####    // From Purple (1, 0, 1) to Blue (0, 0, 1), with increasing intensity (set below)
#####    Red = -(wavelength - 440) / (440 - 350);
#####    Green = 0.0;
#####    Blue  = 1.0;
#####    
#####  } else if (wavelength >= 440 && wavelength < 490) {
#####    // From Blue (0, 0, 1) to Cyan (0, 1, 1) 
#####    Red = 0.0;
#####    Green = (wavelength - 440) / (490 - 440);
#####    Blue  = 1.0;
#####    
#####  } else if (wavelength >= 490 && wavelength < 510) {
#####    // From  Cyan (0, 1, 1)  to  Green (0, 1, 0) 
#####    Red = 0.0;
#####    Green = 1.0;
#####    Blue = -(wavelength - 510) / (510 - 490);
#####    
#####  } else if (wavelength >= 510 && wavelength < 580) { 
#####    // From  Green (0, 1, 0)  to  Yellow (1, 1, 0)
#####    Red = (wavelength - 510) / (580 - 510);
#####    Green = 1.0;
#####    Blue = 0.0;
#####    
#####  } else if (wavelength >= 580 && wavelength < 645) {
#####    // From  Yellow (1, 1, 0)  to  Red (1, 0, 0)
#####    Red = 1.0;
#####    Green = -(wavelength - 645) / (645 - 580);
#####    Blue = 0.0;
#####    
#####  } else if (wavelength >= 645 && wavelength <= 780) {
#####    // Solid Red (1, 0, 0), with decreasing intensity (set below)
#####    Red = 1.0;
#####    Green = 0.0;
#####    Blue = 0.0;
#####    
#####  } else {
#####    Red = 0.0;
#####    Green = 0.0;
#####    Blue = 0.0;
#####  }
##### 
#####  // Intensity factor goes through the range:
#####  // 0.1 (350-420 nm) 1.0 (420-645 nm) 1.0 (645-780 nm) 0.2
##### 
#####  if (wavelength >= 350 && wavelength < 420) {
#####    Factor = 0.1 + 0.9*(wavelength - 350) / (420 - 350);
#####    
#####  } else if (wavelength >= 420 && wavelength < 645) {
#####    Factor = 1.0;
#####    
#####  } else if (wavelength >= 645 && wavelength <= 780) {
#####    Factor = 0.2 + 0.8*(780 - wavelength) / (780 - 645);
#####    
#####  } else {
#####    Factor = 0.0;
#####  }
#####
#####  var R = factorAdjust (Red, Factor, IntensityMax, Gamma);
#####  var G = factorAdjust (Green, Factor, IntensityMax, Gamma);
#####  var B = factorAdjust (Blue, Factor, IntensityMax, Gamma);
#####
#####  //return Color.FromArgb(R, G, B);
#####  //return "R:" + R + ", G:" + G + ", B:" + B;
#####  return "#" + d2h (R,2) + d2h (G,2) + d2h (B,2);
#####}
#####
#####function factorAdjust (color, factor, intensityMax, gamma) {
#####  
#####  if (color == 0.0) {
#####    return 0;
#####  } else {
#####    return Math.round (intensityMax * Math.pow (color * factor, gamma));
#####  }
#####}
#####
#####// Convert a decimal number into hex as a string.
#####// The optional minCharacters gives the minimum number of characters to return.
#####// The result is left-padded with "0" (zeros) to fill ou the string as needed.
#####
#####function d2h (d, minChars) {
#####  var result;
#####
#####  result = d.toString(16);
#####
#####  while (result.length < minChars) {
#####    result = "0" + result;
#####  }
#####  return result;
#####}
#####
#####function h2d (h) {
#####  return parseInt(h,16);
#####} 
#####
#####//private void trackBar1_Scroll(object sender, EventArgs e) { 
#####//   this.panel1.BackColor = getColorFromWaveLength(this.trackBar1.Value); 
#####//   this.label1.Text = this.trackBar1.Value.ToString() + " nm"; 
#####//   this.label2.Text = "R: " + 
#####//   ((Color) getColorFromWaveLength(this.trackBar1.Value)).R.ToString(); 
#####//   this.label3.Text = "G: " + 
#####//   ((Color) getColorFromWaveLength(this.trackBar1.Value)).G.ToString(); 
#####//   this.label4.Text = "B: " + 
#####//   ((Color) getColorFromWaveLength(this.trackBar1.Value)).B.ToString();
#####//}
##### 
      pass
      

    def numberIsColorMethod( self ):
      print self.data
      leftR = ( self.data['left'] >> 5 ) & 0x1f
      leftG = ( self.data['left'] >> 6 ) & 0x3f
      leftB = ( self.data['left'] >> 5 ) & 0x1f

      rightR = ( self.data['right'] >> 5 ) & 0x1f
      rightG = ( self.data['right'] >> 6 ) & 0x3f
      rightB = ( self.data['right'] >> 5 ) & 0x1f

      self.changeWidgetColor( self.wid0, leftR, leftG, leftB )
      self.changeWidgetColor( self.wid2, leftR, leftG, leftB )

      self.changeWidgetColor( self.wid1, rightR, rightG, rightB )
      self.changeWidgetColor( self.wid3, rightR, rightG, rightB )




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
