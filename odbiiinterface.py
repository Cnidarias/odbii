import os
import sys
import time

import usb.core
import usb.util

packet_len = 64


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

    dev.set_configuration( 1 )




if __name__ == '__main__':
    main()

