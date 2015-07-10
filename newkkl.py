import serial



def sendBit( bit, ser ):
    if bit == 1:
        ser.setRTS( True )
        ser.setBreak( False )
        ser.setRTS( False )


    if bit == 0:
        ser.setRTS( True )
        ser.setBreak( True )





def openECU( ser ):

    address = 0x01
    delay = 0.2

    # need to send 0 1000 000 0 1
    # first 0 is start bit 
    # then we have the address 0x01 - but LSB first
    # for 7 bits - cause 7O1 
    # then we send parity bit
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





ser = serial.Serial( '/dev/ttyUSB0', 9600, timeout = 1, rtscts = 1, dsrdtr = 1 )


if not ser.isOpen():
    print "Shit happens"
    return


openECU( ser )


packet = ser.read( 1 )


print packet, ord( packet )
