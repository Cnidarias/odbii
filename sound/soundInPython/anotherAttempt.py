import pyaudio
import wave
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# This is Qt part: we create a window, which has a "stop" flag.
# Stop flag defaults to False, but is set to True, when you press a key.
# Value of that flag is checked in main loop and loop exits when flag is True.

app = QApplication(sys.argv)
class MyWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.stop = False
    def keyPressEvent(self, event):
        print "keyPressedEvent caught!"
        self.stop = True

window = MyWindow()
window.show()

# This is sound processing part: we create an input stream to read from microphone.

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(2),
        channels = 2,
        rate=44100,
        input=True,
        output=False,
        frames_per_buffer=1024)

# This is main loop: we iteratively poll audio and gui: audio data are stored in output_buffer,
# whereas gui is checked for stop flag value (if keyPressedEvent happened, flag will be set
# to True and break our main loop).

output_buffer = ""
while True:
    app.processEvents()
    data = stream.read(1024)
    output_buffer += data
    if window.stop: break

stream.stop_stream()
stream.close()

# Here we output contents of output_buffer as .wav file
output_wav = wave.open("output.wav", 'w')
output_wav.setparams((2, 2, 44100, len(output_buffer),"NONE","not compressed"))
output_wav.writeframesraw(output_buffer)

p.terminate()
