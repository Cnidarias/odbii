import select, socket
import time
import json
import pigpio

import threading

from base64 import b64decode
from sfft import getHZfromSample
from showSound import getRGB

class LEDsetter:
  def __init__( self ):
    self.pins = [
      [[ 27, 0 ], [ 17, 0 ], [ 22, 0 ]], 
      [[ -1, 0 ], [ -1, 0 ], [ -1, 0 ]],
      [[ -1, 0 ], [ -1, 0 ], [ -1, 0 ]],
      [[ -1, 0 ], [ -1, 0 ], [ -1, 0 ]],
      [[ -1, 0 ], [ -1, 0 ], [ -1, 0 ]]
      ]

    self.pi = pigpio.pi()

    self.over_all_brightness = 255

  def getPinLayout( self ):
    return self.pins 

  def setColorOfPin( self, pin, brightness ):
    if pin == -1: return 
    if brightness > 255: brightness = 255
    elif brightness < 0: brightness = 0

    self.pi.set_PWM_dutycycle( pin, brightness * (self.over_all_brightness/255) )


  def updateAll( self ):
    for strip in self.pins:
      r,g,b = strip
      self.setColorOfPin( r[0], r[1] )
      self.setColorOfPin( g[0], g[1] )
      self.setColorOfPin( b[0], b[1] )


  def setColorMatrix( self, colors ):
    i = 0
    for strip in self.pins:
      strip[0][1] = colors[i][0]
      strip[1][1] = colors[i][1]
      strip[2][1] = colors[i][2]
      i += 1



  
class getDataOverUDP():
  def __init__( self ):
    self.ledSetter = LEDsetter()
    self.rgbGetter = getRGB()
    self.colors = None

    self.PORT = 12345
    self.IP = "0.0.0.0"
    self.bufferSize = 4096
    self.s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    self.s.bind( ( self.IP, self.PORT ) )

    self.getData()

  def process_command(self, data):
    self.ledSetter.over_all_brightness = data['brightness']

  def getData( self ):
    while True:
      data, addr = self.s.recvfrom( self.bufferSize )
      jsonData = json.loads( data )
      if jsonData['type'] == 'data':
        self.ledSetter.setColorMatrix( self.rgbGetter.shadesOfColorCircle( jsonData, False ) )
        self.ledSetter.updateAll()
      else:
        self.process_command(jsonData)
        self.s.sendto(json.dumps({'type': 'status_received'}), (self.IP, self.PORT))



if __name__ == '__main__':
    ex = getDataOverUDP()
