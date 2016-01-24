import pyaudio
from struct import *

p = pyaudio.PyAudio()

stream = p.open( format = p.get_format_from_width( 2 ),
        channels = 2,
        rate = 44100,
        input = True,
        output = False,
        frames_per_buffer = 1024 )

output_buffer = ""

while True:
    data = stream.read( 1024 )
    i = 0
    r = unpack( '2048h', data )

    print r
