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
    self.state = 0
    self.ecuOpen = -1
    address = ( 'localhost', 6000 )
    self.data = data


  def run( self ):
    try:
        self.ser = serial.Serial( '/dev/ttyUSB0', 9600 , timeout = 1, rtscts = 1, dsrdtr = 1 )
        self.packetCounter = 0

        self.state = 1
        self.mainRunner()
    except:
        if self.ser is not None:
            self.ser.close()
        #raise
        return


  def bitFlip( self, n ):
      return chr( 0xff ^ n )
  
  
  def sendBit( self, bit ):
      if bit == 1:
          self.ser.setRTS( True )
          self.ser.setBreak( False )
          self.ser.setRTS( False )
  
      if bit == 0:
          self.ser.setRTS( True )
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


  def sendQuitBlock( self ):
      if self.packetCounter == 0xff:
          self.packetCounter = 0
      else:
          self.packetCounter += 1

      self.ser.write( '\x03' )
      self.ser.read( 1 )

      packet = self.ser.read( 1 ) # should be 0x03 compliment

      self.ser.write( chr( self.packetCounter ) )
      packet = self.ser.read( 1 ) # should be self.packetCounter kompliment
      
      self.ser.write( '\x06' )
      self.ser.read( 1 )

      packet = self.ser.read( 1 ) # should be 0x06 compliment

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
      #print "MESSAGE LEN\t " + str( messageLen )
      self.ser.write( self.bitFlip( messageLen ) )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 )
      self.packetCounter = ord( packet )
      #print "PACKET CTR\t " + str( self.packetCounter )
      self.ser.write(self.bitFlip( self.packetCounter ) )
      packet = self.ser.read( 1 )
  
      packet = self.ser.read( 1 )
      blockTitle = ord( packet )
      self.ser.write( self.bitFlip( blockTitle ) )
      packet = self.ser.read( 1 )

      #print "THIS IS BLOCKTITLE\t" + str( blockTitle )
  
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
          return "ACK"
  
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
          return self.humanReadableVals(result)
  ####################################################
  
  

  def humanReadableVals( self, array ):
      message = "READABLE CAR RET: "
      i = 0
      print array
      while i < len( array ) / 3 :
          index = i * 3
          a = array[index + 1]
          b = array[index + 2]
          if self.state == 1:

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
                self.data['usage'] = 0.001 * a * b 
            else:
                message += str( array[index] ) + '\t'

          elif self.state == 2:

            if array[index] == 1: 
                message += "RPM " + str( 0.2 * a * b ) + "\t"
                self.data['rpm'] = 0.2 * a * b
            elif array[index] == 5:
                message += "outsideTmp" + str( a * ( b - 100 ) * 0.1 ) + "\t"
            elif array[index] == 7:
                message += "km/h " + str( 0.01 * a * b ) + "\t"
                self.data['speed'] = 0.01 * a * b
            elif array[index] == 19:
                message += "fuel l " + str( a * b * 0.01 ) + "\t"
                self.data['gas'] = a * b * 0.01 
            elif array[index] == 36:
                message += "Mileage km " + str( a * 2560 + b * 10 ) + "\t"
                self.data['mileage'] = a * 2560 + b * 10 
            elif array[index] == 44:
                message += "Time " + str( a ) + ":" + str( b ) + "\t"
                self.data['time'] = str( a ) + ":" + str( b )
            else:
                message += "Unknown" + str( array[index] )

          i += 1
  
      print self.data
      return message
  
  
  def mainRunner( self ):
     while True:
          # this needs to be revamped
          if self.state == 1:
            if self.ecuOpen != 0x01:
              self.openECU( 0x01 )
              self.ecuOpen = 0x01
            self.sendACKBlock()
            print self.readBlock()
            self.requestDataBlock(0x03)
            print self.readBlock()
            self.requestDataBlock(0x0b)
            print self.readBlock()

            #self.sendQuitBlock()
            #self.state = 2
          
          if self.state == 2:
            if self.ecuOpen != 0x17:
              self.openECU( 0x17 )
              self.ecuOpen = 0x17
            self.sendACKBlock()
            print self.readBlock()
            self.requestDataBlock(0x01)
            print self.readBlock()

            #self.sendQuitBlock()
            #self.state = 1
 


  def openECU( self, address = 0x01 ):
      delay = 0.2
  
      # For ECU Address 0x01:
      # need to send 0 1000 000 0 1
  
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
      
      # read the bits you sent to "clear" buffer
  
      # Read stuff that we do not /really/ care about

      # Kennungs ID
  
      print address

      if address == 0x01:
        packet = self.ser.read( 1 )
        while ord( packet ) != 0x8a:
          packet = self.ser.read( 1 )
          print str( address ) +"\t"+ str( ord( packet ) )
      else:
        packet = self.ser.read( 1 )
        while ord( packet ) != 0x8a:
          packet = self.ser.read( 1 )
          print str( address ) +"\t"+ str( ord( packet ) )
        packet = self.ser.read( 1 )
        while ord( packet ) != 0x8a:
          packet = self.ser.read( 1 )
          print str( address ) +"\t"+ str( ord( packet ) )
      self.ser.write( self.bitFlip( ord( packet ) ) )
      packet = self.ser.read( 1 ) # always throws same packet back at us
  
      message = self.readBlock()

      # Keep on reading String messages that the ECU sends us, until
      # it is finally done telling us who it is
      # then simply send another ACK block and start reading data - easy
      while message is not "ACK":
        print  "This is a message" 
        print message 
        self.sendACKBlock() # self.send ack block confimration
        message = self.readBlock()
  
      self.sendACKBlock()
      print self.readBlock()

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
  
      #self.mainRunner()
     

#############################################################################
def main():
  data = {'speed' : 200, 'rpm': 2000, 'fuel': 10, 'mileage': 10, 'time' : "12:12", 'usage' : 3.5  }
  task = kw1281( data )
  task.start()
   
if __name__ == "__main__":
    main()
