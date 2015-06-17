import os
import sys
import time

import usb.core
import usb.util

packet_len = 64


def show_result(bytes):
        sys.stdout.write( "Result:" )
        sys.stdout.write( ''.join( ['%s ' % hex(abyte) for abyte in bytes] ) )
        sys.stdout.write( '\n' )

# add function protokols here


def main():

    dev = usb.core.find( idVendor=0x0403, idProduct=0x6001 )

    if dev is None:
        raise ValueError( 'Device not found!' )

    try:  # if Kernel Driver has been loaded, unload it.
        dev.detach_kernel_driver( 0 )
    except: # prolly no Kernel Driver was ever loaded so ignore
        pass

    # Set active configuration - Remember to check with lsusb -v -d vendorID:

    # this is basically lsusb -v 
    print dev

    dev.set_configuration( 1 )


    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]
    ep = usb.util.find_descriptor( 
            intf,
            # math first OUT endpoint
            custom_match = \
                    lambda e: \
                    usb.util.endpoint_direction( e.bEndpointAddress ) == \
                    usb.util.ENDPOINT_OUT )
    if ep is None:
        raise ValueError( 'No ENDPOINT_OUT found' )

    ep.write( '03\r' );
    
    byte = dev.read( 0x81, packet_len, 100 )
    show_result( byte )


    ep.write( '010D\r' );
    byte = dev.read( 0x81, packet_len, 100 )
    show_result( byte )

if __name__ == '__main__':
    main()

