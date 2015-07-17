import Queue
import threading
from multiprocessing.connection import Client

class tester(threading.Thread):
  def __init__(self, data ):
    threading.Thread.__init__(self)
    self.data = data
    self.i = 0
  def run( self ):
    while True:
      self.i += 1
      if self.i > 10000:
        self.i = 0
      self.data['rpm'] = self.i
      self.data['speed'] = self.i ^ 0xf9

