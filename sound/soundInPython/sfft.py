import subprocess

from scipy.signal import blackmanharris
from struct import unpack
from parabolic import parabolic
import numpy as np
import time


import soundProcessor

class getHZfromSample:
    def __init__( self ):
        pass

    def getHz ( self, soundData, rate ):
        usedata = unpack( "%dh" % ( len( soundData ) / 2 ), soundData )
        usedata = np.array( usedata, dtype='h')
        window = usedata * blackmanharris( len( usedata ) )
        fouriour = np.fft.rfft( window )
        fouriour = np.delete( fouriour, len( fouriour ) -1 )
        
        i = np.argmax( abs( fouriour ) )
        true_i = parabolic( np.log( abs( fouriour ) ), i )[0]
        
        return rate * true_i / len( window )
        
def main():
    data = { 'left' : 0, 'right' : 0 }
    task = soundProcessor.getSound( data )
    task.daemon = True
    task.start()

    time.sleep( 2 )

    while True:

        usedata = unpack( "%dh"%(len(data['all'])/2), data['all'] )
        usedata = np.array( usedata, dtype='h')
        window = usedata * blackmanharris( len( usedata ) )
        fouriour = np.fft.rfft( window )
        fouriour = np.delete( fouriour, len( fouriour ) -1 )
        
        i = np.argmax( abs( fouriour ) )
        true_i = parabolic( np.log( abs( fouriour ) ), i )[0]

        print 44100 * true_i / len( window )
        


if __name__ == '__main__':
    main()
