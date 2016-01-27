import select, socket


class LEDsetter:
    def __init__( self ):
        self.port = 53005
        self.bufferSize = 1024
        self.s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.s.bind( ( '', self.port ) )
        self.s.setblocking( 0 )

        self.getData()

    def getData( self ):
        while True:
            print "test"
            result = select.select( [self.s], [], [] )
            print result
            #msg = result[0][0].recvall( self.bufferSize )
            #print msg



if __name__ == '__main__':
    ex = LEDsetter()
