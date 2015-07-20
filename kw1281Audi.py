import os
import serial
import time
import struct
import sys
import threading


class kw1281( threading.Thread ):
  def __init__ ( self, data ):
    threading.Thread.__init__( self )
    self.ser = None
    address = ( 'localhost', 6000 )
    self.data = data


  def run( self ):
    try:
        self.ser = serial.Serial( '/dev/ttyUSB0', 9600 , timeout = 1, rtscts = 1, dsrdtr = 1 )
        self.packetCounter = 0
        self.openECU()
    except:
        if self.ser is not None:
            self.ser.close()
        raise


  def bitFlip( self, n ):
      return chr( 0xff ^ n )
  
  
  def sendBit( self, bit ):
      if bit == 1:
          self.ser.setRTS( True )
          self.ser.setBreak( False )
          self.ser.write('\xff')
          self.ser.setRTS( False )
  
      if bit == 0:
          self.ser.setRTS( True )
          self.ser.write('\x00')
          self.ser.setBreak( True )
  
  
  def sendACKBlock( self ):
      if self.packetCounter == 0xff:
          self.packetCounter = 0
      else:
          self.packetCounter += 1
  
      self.ser.write( '\x03' )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 ) # should be 0x03 kompliment
  
      self.ser.write( chr( self.packetCounter ) )
      packet = self.ser.read( 1 )
      packet = self.ser.read( 1 ) # should be self.packetCounter kompliment
  
      self.ser.write( '\x09' ) # this is the block command
      packet = self.ser.read( 1 )
      packet = self.ser.read( 1 ) # should be the 0x09 kompliment
  
      self.ser.write( '\x03' )
      packet = self.ser.read( 1 )
  
  
  def requestDataBlock( self, block ):
      if self.packetCounter == 0xff:
          self.packetCounter = 0
      else:
          self.packetCounter += 1
  
      self.ser.write( '\x04' )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 ) # this is the 0x04 kompliment
  
      self.ser.write( chr( self.packetCounter ) )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 ) # this is the kompliment of the self.packetCounter
  
      self.ser.write( '\x29' ) # this is the command for a grp reading
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 ) # this is the compliment of 0x29
  
      # now send the grp ID number --
      self.ser.write( chr( block ) )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 ) # should be compliment - yet again
  
      self.ser.write( '\x03' )
      packet = self.ser.read( 1 )
  
  
  
  def readBlock( self ):
      #################################################
      packet = self.ser.read( 1 )
      messageLen = ord( packet )
      self.ser.write( self.bitFlip( messageLen ) )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 )
      self.packetCounter = ord( packet )
      self.ser.write(self.bitFlip( self.packetCounter ) )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 )
      blockTitle = ord( packet )
      self.ser.write( self.bitFlip( blockTitle ) )
      packet = self.ser.read( 1 )
  
      if blockTitle == 0xf6:
          i = 3
          message = ""
  
          while i < messageLen:
              packet = self.ser.read( 1 )
              message += packet
  
              self.ser.write( self.bitFlip( ord( packet ) ) )
              packet = self.ser.read( 1 )
              i += 1
  
          packet = self.ser.read( 1 ) # read 0x03 end block 
          return message
  
      elif blockTitle == 0x09:
          packet = self.ser.read( 1 ) # read 0x03 end block 
          return ""
  
      elif blockTitle == 0xe7:
          i = 3
          result = []
          while i < messageLen:
              packet = self.ser.read( 1 )
              result.append( ord( packet ) )
              self.ser.write( self.bitFlip( ord( packet ) ) )
              packet = self.ser.read( 1 )
              i += 1
  
          packet = self.ser.read( 1 ) # read 0x03 end block 
          return self.humanReadAbleABVals(result)
  ####################################################
  
  

  def humanReadAbleABVals( self, array ):
      message = ""
      i = 0
      while i < 4:
          index = i * 3
          a = array[index + 1]
          b = array[index + 2]
          if array[index] == 1: 
              message += "RPM " + str( 0.2 * a * b ) + "\t"
              self.data['rpm'] = 0.2 * a * b
          elif array[index] == 5: 
              message += "deg C " + str( a * ( b - 100 ) * 0.1 ) + "\t"
          elif array[index] == 7: 
              message += "km/h " + str( 0.01 * a * b ) + "\t"
              self.data['speed'] = 0.01 * a * b
          elif array[index] == 21: 
              message += "V " + str( 0.001 * a * b ) + "\t"
          elif array[index] == 22: 
              message += "??? " + str( 0.001 * a * b ) + "\t"
          elif array[index] == 35: 
              message += "l/h " + str( 0.01 * a * b ) + "\t"
            #message += str( array[index] ) + '\t'
          i += 1
  
      print self.data
      return message
  
  
  
  
  
  def openECU( self ):
  
      address = 0x01
      delay = 0.2
  
      # need to send 0 1000 000 0 1
      # first 0 is start bit 
      # then we have the address 0x01 - but LSB first
      # for 7 bits - cause 7O1 
      # then we send odd parity bit
      # then we send stop bit 
      # should be easy enough right?
  
      self.sendBit( 0 )
      time.sleep( delay )
  
      p = 1
      for i in xrange( 0, 7 ):
          bit = ( address >> i ) & 0x01
          self.sendBit( bit )
  
          p ^= bit
  
          time.sleep( delay )
  
      self.sendBit( p )
      time.sleep( delay )
  
      self.sendBit( 1 )
      time.sleep( delay )
  
      self.ser.setRTS( False )
      self.ser.setDTR( True )
  
      time.sleep( 0.5 )
  
  
      self.ser.setRTS( True )
      self.ser.setDTR( True )
      self.ser.setBreak( False )
  
      packet = self.ser.read( 4 )
  
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 ) 
  
      self.ser.write( self.bitFlip( ord( packet ) ) )
      packet = self.ser.read( 1 ) # always throws same packet back at us
  
      message = self.readBlock()
      print "VAG-Nummer:", message
      self.sendACKBlock() # self.send ack block confimration
  
      message = self.readBlock()
      print "Engine:", message
      self.sendACKBlock()
  
      message = self.readBlock()
      print "Software Coding:", message
      self.sendACKBlock()
  
      message = self.readBlock()
      print "Type:", message
      self.sendACKBlock()
  
      # NOW we have handeled basic communication -
      # We now self.send ACK commands back and forth - forever
  
      # test all avaibale packets we could self.read
      #tester = 1
      #while tester <= 255:
      #  try:
      #    print tester, self.readBlock()
      #    self.sendACKBlock()
      #    print self.readBlock()
      #    requestDataBlock( tester )
      #    tester += 1
      #  except:
      #    break
  
      while True:
          print self.readBlock()
          self.sendACKBlock()
          print self.readBlock()
          self.requestDataBlock(0x03)
          print self.readBlock()
          self.requestDataBlock(0x0b)



#############################################################################
def main():
  data = {'speed' : 200, 'rpm': 2000}
  task = kw1281( data )
  task.start()
   
if __name__ == "__main__":
    main()
