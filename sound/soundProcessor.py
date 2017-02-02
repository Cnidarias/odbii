### PAVUCONTROL ###
import os
import time
import threading
import pyaudio
import audioop

from socket import *
import json

from struct import *
from numpy import mean

from base64 import b64encode
from sfft import getHZfromSample

class getSound(threading.Thread):
  def __init__(self, data):
    threading.Thread.__init__(self)


    self.command_status = { 'brightness': 0, 'type': 'command' }
    self.sending_command = False

    self.data = data 
    self.p = pyaudio.PyAudio()

    self.rate = 12000


    self.mkHz = getHZfromSample()


    self.cs = socket(AF_INET, SOCK_DGRAM)
    self.IP = "0.0.0.0"
    self.PORT = 12345
    self.cs.bind((self.IP, self.PORT))


    self.stream = self.p.open(format = self.p.get_format_from_width(2),
        channels = 2,
        rate = self.rate,
        input = True,
        output = False,
        frames_per_buffer = 512)


  def getSoundData(self):
    soundData = self.stream.read(512)
    r = unpack('1024h', soundData)
    i = 0
    left = 0
    right = 0
    while i < len(r):
      left += r[i]
      right += r[i+1]
      i += 2

    j = 0

    l = b''
    r = b''
    while j < len(soundData):
      r += soundData[j:j+2]
      l += soundData[j+2:j+4]
      j += 4


    left = left / (len(r) / 2)
    right = right / (len(r) / 2)


    lfreq = self.mkHz.getHz(l, self.rate)
    rfreq = self.mkHz.getHz(r, self.rate)

    #self.data['leftAll'] = b64encode(l)
    #self.data['rightAll'] = b64encode(r)

    self.data['leftAll'] = lfreq
    self.data['rightAll'] = rfreq
    self.data['loudness'] = audioop.rms(soundData, 2)
    self.cs.sendto(json.dumps(self.data), (self.IP, self.PORT))



  def set_brightness(self, brightness):
    self.sending_command = True
    self.command_status['brightness'] = brightness


  def run(self):
    while True:
      if not self.sending_command:
        self.getSoundData()
      else:
        self.cs.sendto(json.dumps(self.command_status), (self.IP, self.PORT))

        data, addr = self.cs.recvfrom(1024)
        jsonData = json.loads(data)

        if jsonData['type'] == 'status_received':
          self.sending_command = False


def main():
  data = { 'left': 0, 'right': 0, 'type': 'data' }
  task = getSound(data)
  task.start()

if __name__ == '__main__':
  main()
