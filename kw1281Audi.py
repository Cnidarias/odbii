import serial
import time
import struct


def bitFlip( n ):
  return chr( 0xff ^ n )


def sendBit( bit, ser ):
  if bit == 1:
    ser.setRTS( True )
    ser.setBreak( False )
    ser.write('\xff')
    ser.setRTS( False )


  if bit == 0:
    ser.setRTS( True )
    ser.write('\x00')
    ser.setBreak( True )





def openECU( ser ):

  address = 0x01
  delay = 0.2

  # need to send 0 1000 000 0 1
  # first 0 is start bit 
  # then we have the address 0x01 - but LSB first
  # for 7 bits - cause 7O1 
  # then we send odd parity bit
  # then we send stop bit 
  # should be easy enough right?

  sendBit( 0, ser )
  time.sleep( delay )

  p = 1
  for i in xrange( 0, 7 ):
    bit = ( address >> i ) & 0x01
    sendBit( bit, ser )

    p ^= bit

    time.sleep( delay )

  sendBit( p, ser )
  time.sleep( delay )

  sendBit( 1, ser )
  time.sleep( delay )

  ser.setRTS( False )
  ser.setDTR( True )

  time.sleep( 0.5 )


  ser.setRTS( True )
  ser.setDTR( True )
  ser.setBreak( False )

  packet = ser.read( 4 )

  packet = ser.read( 1 )

  packet = ser.read( 1 )

  packet = ser.read( 1 ) 

  print hex( ord( packet ) )
  flip = bitFlip( ord( packet ) )
  ser.write( flip )
  packet = ser.read( 1 ) # always throws same packet back at us


  packet = ser.read( 1 )
  messageLen = ord( packet )
  ser.write( bitFlip( messageLen ) )
  packet = ser.read( 1 )

  packet = ser.read( 1 )
  blockCounter = ord( packet )
  ser.write( bitFlip( blockCounter ) )
  ser.read( 1 )

  packt = ser.read( 1 )
  ser.write( bitFlip( ord( packet ) ) )
  ser.read( 1 )


  i = 1
  message = ""
  while i < messageLen:
    i += 1
    packet = ser.read( 1 )
    print hex( ord(packet))
    message += packet

    ser.write( bitFlip( ord( packet ) ) )
    packet = ser.read( 1 )
  

  print message







ser = serial.Serial( '/dev/ttyUSB0', 9600 , timeout = 1, rtscts = 1, dsrdtr = 1 )


if not ser.isOpen():
  print "Shit happens"


openECU( ser )




ser.close()
