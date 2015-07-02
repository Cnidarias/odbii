import sys
import time
import bluetooth
from pprint import pprint 

def readPacket():
    global sock
    try:
        while True:
            msg = sock.recv( 1024 )
            msg = msg.split( "," )

            lat, lng = None, None

            if msg[0] == "$GPGGA":
                lat = msg[2] + msg[3]
                lng = msg[4] + msg[5]
            elif msg[0] == "$GPRMC":
                lat = msg[3] + msg[4]
                lng = msg[5] + msg[6]


            if lat is not None and lng is not None:
                lat = lat[:2] + " " + lat[2:]
                lng = lng[:3] + " " + lng[3:]
                print lat, lng

    except bluetooth.btcommon.BluetoothError as e:
        print e
        print "Lost connection!"
        print "Retrying to get connection"
        connectToDevice()



def connectToDevice():
    global sock
    global port
    global target_addr
    while True:
        try:
            sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            sock.connect( (target_addr,port ) )
            print "Connected - Now trying to read GPS data!"
            readPacket()
            break
        except bluetooth.btcommon.BluetoothError as e:
            print e
            if '112' in e:
                print "Seems like your BT is not enabled!"
            if '111' in e:
                print "Seems like BlueNMEA is not enabled/functioning correctly please re/start it!"
            time.sleep( 5 )
                    

def convertGooglePolyLine( line ):
    index = 0
    length = len( line )
    lat, lng = 0, 0 

    while index < length:
        b = 0
        shift = 0
        result = 0

        while True:
            b = ord( line[index] ) - 63
            index += 1

            result |= ( b & 0x1f ) << shift;
            shift += 5

            if b < 0x20: break

        if result & 1 != 0:
            lat += ~( result >> 1 )
        else:
            lat += result >> 1

        shift = 0
        result = 0

        while True:
            b = ord( line[index] ) - 63
            index += 1

            result |= ( b & 0x1f ) << shift;
            shift += 5

            if b < 0x20: break

        if result & 1 != 0:
            lng += ~( result >> 1 )
        else:
            lng += result >> 1


        print "{0:.5f}".format( lat / 100000.0 ), "{0:.5f}".format( lng / 100000.0 )






sock = None
target_addr = "90:68:C3:82:78:78"
port = 5


print "\n\n\n"
convertGooglePolyLine( "_p~iF~ps|U_ulLnnqC_mqNvxq`@" )
print "\n\n\n"
convertGooglePolyLine( "yimrHg}ep@JDBOLy@No@j@{Ad@kAV}AB{@?oAC_AEu@O}BC[GKMsBK}AGiAKiBm@cIq@cOIoBG_BCk@Cq@Aw@?mD?WB_CL}EFwBCcACm@Ic@Kg@Ky@I]Ok@Qe@Wq@O]KS" )
print "\n\n\n"
convertGooglePolyLine( "}nmrHekip@?A@A?A@A?A?A@A?A?A?A?A?A@C?A?A?AAA?A?A?A?AAA?AAC?AAA?AAA?AA??AA?AAAAA?AAA?A?A?A?A@A?A??@A?A@?@A??@A@A@?@A@?@A@?@?@?@A@?@?@?B?@?@?@?@?@?@@@?@?@?@@??@WVqB`BIH{@z@i@h@c@j@MTSZOXMXQd@O^M`@Mh@IZG\\I^G\\G\\G^G^Mp@SlAG\\Ox@I\\K^K^Ur@Yr@[p@]n@U^KPKPQX}BxDeBrCOTGHIHGHIFGFSNIFGFIDwBjAaCpAOH{C`BwBjAOFOFMDM@U@OA[Gg@G[EKCEASEOIGEEGGKMU" )
print "\n\n\n"

connectToDevice()
