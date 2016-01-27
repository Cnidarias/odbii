### PAVUCONTROL ###
import os
import time
import threading
import pyaudio
from struct import *
from numpy import mean

class getSound( threading.Thread ):
  def __init__( self, data ):
    threading.Thread.__init__( self )

    self.data = data 
    self.p = pyaudio.PyAudio()

    self.stream = self.p.open( format = self.p.get_format_from_width( 2 ),
        channels = 2,
        rate = 44100,
        input = True,
        output = False,
        frames_per_buffer = 512 )

  def run( self ):
    while True:
      soundData = self.stream.read( 512 )
      r = unpack( '1024h', soundData )
      i = 0
      left = 0
      right = 0
      while i < len( r ):
        left += r[i]
        right += r[i+1]
        i += 2

      j = 0

      l = b''
      r = b''
      while j < len( soundData ):
        l += soundData[j:j+2]
        r += soundData[j+2:j+4]
        j += 4


      left = left / ( len( r ) / 2 )
      right = right / ( len( r ) / 2 )

      self.data['leftAll'] = l
      self.data['rightAll'] = r
      self.data['left'] = left
      self.data['right'] = right
      self.data['all'] = soundData


def main():
  data = { 'left': 0, 'right': 0 }
  task = getSound( data )
  task.start()

if __name__ == '__main__':
  main()
