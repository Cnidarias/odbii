import os
import serial
import time
import struct
import sys
from multiprocessing.connection import Client


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

    ser.write( chr( packetCounter ) )
    packet = ser.read( 1 )
    packet = ser.read( 1 ) # should be packetCounter kompliment

    ser.write( '\x09' ) # this is the block command
    packet = ser.read( 1 )
    packet = ser.read( 1 ) # should be the 0x09 kompliment

    ser.write( '\x03' )
    packet = ser.read( 1 )


def requestDataBlock( block ):
    global ser
    global packetCounter

    if packetCounter == 0xff:
        packetCounter = 0
    else:
        packetCounter += 1

    ser.write( '\x04' )
    packet = ser.read( 1 )

    packet = ser.read( 1 ) # this is the 0x04 kompliment

    ser.write( chr( packetCounter ) )
    packet = ser.read( 1 )

    packet = ser.read( 1 ) # this is the kompliment of the packetCounter

    ser.write( '\x29' ) # this is the command for a grp reading
    packet = ser.read( 1 )

    packet = ser.read( 1 ) # this is the compliment of 0x29

    # now send the grp ID number --
    ser.write( chr( block ) )
    packet = ser.read( 1 )

    packet = ser.read( 1 ) # should be compliment - yet again

    ser.write( '\x03' )
    packet = ser.read( 1 )








def readBlock():
    global ser
    global packetCounter

    #################################################
    packet = ser.read( 1 )
    messageLen = ord( packet )
    ser.write( bitFlip( messageLen ) )
    packet = ser.read( 1 )

    packet = ser.read( 1 )
    packetCounter = ord( packet )
    ser.write( bitFlip( packetCounter ) )
    packet = ser.read( 1 )

    packet = ser.read( 1 )
    blockTitle = ord( packet )
    ser.write( bitFlip( blockTitle ) )
    packet = ser.read( 1 )

    if blockTitle == 0xf6:
        i = 3
        message = ""

        while i < messageLen:
            packet = ser.read( 1 )
            message += packet

            ser.write( bitFlip( ord( packet ) ) )
            packet = ser.read( 1 )
            i += 1

        packet = ser.read( 1 ) # read 0x03 end block 
        return message

    elif blockTitle == 0x09:
        packet = ser.read( 1 )
        return ""

    elif blockTitle == 0xe7:
        i = 3
        result = []
        while i < messageLen:
            packet = ser.read( 1 )
            result.append( ord( packet ) )
            ser.write( bitFlip( ord( packet ) ) )
            packet = ser.read( 1 )
            i += 1

        packet = ser.read( 1 ) # read 0x03 end block 
        return humanReadAbleABVals(result)

####################################################


def humanReadAbleABVals( array ):
    message = ""
    i = 0
    while i < 4:
        index = i * 3
        a = array[index + 1]
        b = array[index + 2]
        if array[index] == 1: 
            message += "RPM " + str( 0.2 * a * b ) + "\t"
            conn.send( ['RPM', 0.2*a*b] )
        elif array[index] == 5: 
            message += "deg C " + str( a * ( b - 100 ) * 0.1 ) + "\t"
            conn.send( ['TMP', a * ( b - 100 ) * 0.1] )
        elif array[index] == 7: 
            message += "km/h " + str( 0.01 * a * b ) + "\t"
            conn.send( ['SPEED', 0.01*a*b] )
        elif array[index] == 21: 
            message += "V " + str( 0.001 * a * b ) + "\t"
            conn.send( ['V', 0.001*a*b] )
        elif array[index] == 22: 
            message += "??? " + str( 0.001 * a * b ) + "\t"
        elif array[index] == 35: 
            message += "l/h " + str( 0.01 * a * b ) + "\t"
            conn.send( ['LH', 0.001*a*b] )
          #message += str( array[index] ) + '\t'
        i += 1

    return message





def openECU():
    print "OPEN ECU REACHED"
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

    message = readBlock()
    print "VAG-Nummer:", message
    sendACKBlock() # send ack block confimration

    message = readBlock()
    print "Engine:", message
    sendACKBlock()

    message = readBlock()
    print "Software Coding:", message
    sendACKBlock()

    message = readBlock()
    print "Type:", message
    sendACKBlock()

    # NOW we have handeled basic communication -
    # We now send ACK commands back and forth - forever

    # test all avaibale packets we could read
    #tester = 1
    #while tester <= 255:
    #  try:
    #    print tester, readBlock()
    #    sendACKBlock()
    #    print readBlock()
    #    requestDataBlock( tester )
    #    tester += 1
    #  except:
    #    break

    while True:
        print readBlock()
        sendACKBlock()
        print readBlock()
        requestDataBlock(0x03)
        print readBlock()
        requestDataBlock(0x0b)



#############################################################################
def main():
    address = ( 'localhost', 6000 )
    # First we open the Serial
    conn = Client( address, authkey='kw1281Audipass' ) 
    ser = serial.Serial( '/dev/ttyUSB0', 9600 , timeout = 1, rtscts = 1, dsrdtr = 1 )
    packetCounter = 0
    openECU()

    conn.send( 'Error' )
    conn.close()
    ser.close()
    sys.exit( 0 )


if __name__ == "__main__":
    main()
