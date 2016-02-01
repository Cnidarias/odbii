import select, socket
import time
import json

from base64 import b64decode

class LEDsetter:
    def __init__( self ):
        self.PORT = 12345
        self.IP  = "127.0.0.1"
        self.bufferSize = 4096
        self.s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.s.bind( ( self.IP, self.PORT ) )

        self.getData()

    def getData( self ):
        while True:
            data, addr = self.s.recvfrom( self.bufferSize )
            jsonData = json.loads( data )
            print b64decode( jsonData['leftAll'] )



if __name__ == '__main__':
    ex = LEDsetter()
