import serial
import time
import struct


def bitFlip( n ):
  return chr( 0xff ^ n )


def sendBit( bit ):
  global ser
  if bit == 1:
    ser.setRTS( True )
    ser.setBreak( False )
    ser.write('\xff')
    ser.setRTS( False )


  if bit == 0:
    ser.setRTS( True )
    ser.write('\x00')
    ser.setBreak( True )


def sendACKBlock():
  global ser
  global packetCounter

  if packetCounter == 0xff:
    packetCounter = 0
  else:
    packetCounter += 1

  ser.write( '\x03' )
  packet = ser.read( 1 )
  
  packet = ser.read( 1 ) # should be 0x03 kompliment
  print hex( ord( packet ) )

  ser.write( chr( packetCounter ) )
  packet = ser.read( 1 )
  packet = ser.read( 1 ) # should be packetCounter kompliment
  print hex( ord( packet ) )

  ser.write( '\x09' ) # this is the block command
  packet = ser.read( 1 )
  packet = ser.read( 1 ) # should be the 0x09 kompliment
  print hex( ord( packet ) )

  ser.write( '\x03' )
  packet = ser.read( 1 )


  


def openECU():
  global ser
  global packetCounter

  address = 0x01
  delay = 0.2

  # need to send 0 1000 000 0 1
  # first 0 is start bit 
  # then we have the address 0x01 - but LSB first
  # for 7 bits - cause 7O1 
  # then we send odd parity bit
  # then we send stop bit 
  # should be easy enough right?

  sendBit( 0 )
  time.sleep( delay )

  p = 1
  for i in xrange( 0, 7 ):
    bit = ( address >> i ) & 0x01
    sendBit( bit )

    p ^= bit

    time.sleep( delay )

  sendBit( p )
  time.sleep( delay )

  sendBit( 1 )
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

  ser.write( bitFlip( ord( packet ) ) )
  packet = ser.read( 1 ) # always throws same packet back at us


  packet = ser.read( 1 )
  messageLen = ord( packet )
  ser.write( bitFlip( messageLen ) )
  packet = ser.read( 1 )

  packet = ser.read( 1 )
  packetCounter = ord( packet )
  ser.write( bitFlip( packetCounter ) )
  packet = ser.read( 1 )

  packet = ser.read( 1 )
  ser.write( bitFlip( ord( packet ) ) )
  packet = ser.read( 1 )


  i = 3
  message = ""

  while i < messageLen:
    packet = ser.read( 1 )
    message += packet

    ser.write( bitFlip( ord( packet ) ) )
    packet = ser.read( 1 )
    i += 1
  

  print "VAG-Nummer:", message

  packet = ser.read( 1 ) # read 0x03 end block 

  sendACKBlock() # send ack block confimration







ser = serial.Serial( '/dev/ttyUSB0', 9600 , timeout = 1, rtscts = 1, dsrdtr = 1 )
packetCounter = 0

openECU()

ser.close()
