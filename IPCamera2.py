"""import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError

class Cam():

  def __init__(self, url):
    
    self.stream = requests.get(url, stream=True)
    self.thread_cancelled = False
    self.thread = Thread(target=self.run)
    print ("camera initialised")

    
  def start(self):
    self.thread.start()
    print ("camera stream started")
    
  def run(self):
    bytes=''
    while not self.thread_cancelled:
      try:
        bytes+=self.stream.raw.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
          jpg = bytes[a:b+2]
          bytes= bytes[b+2:]
          img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
          cv2.imshow('cam',img)
          if cv2.waitKey(1) ==27:
            exit(0)
      except ThreadError:
        self.thread_cancelled = True
        
        
  def is_running(self):
    return self.thread.isAlive()
      
    
  def shut_down(self):
    self.thread_cancelled = True
    #block while waiting for thread to terminate
    while self.thread.isAlive():
      time.sleep(1)
    return True

  
    
if __name__ == "__main__":
  url = 'http://192.168.1.64/?action=stream'
  cam = Cam(url)
  cam.start()

  """

import cv2
import urllib
import numpy as np
from vision import GoalFinder
from networktables import NetworkTable
import datetime
from time import sleep

from networktables2 import NumberArray
import logging
logging.basicConfig(level=logging.DEBUG)

def main():

    ip = "192.168.1.64"
    NetworkTable.setIPAddress(ip)
    NetworkTable.setClientMode()

    #print "Initializing Network Tables"
    NetworkTable.initialize()

    goalFinder = GoalFinder()
    
    stream = urllib.urlopen('http://192.168.1.64/mjpg/video.mjpg')
    bytes = ''

    #print "Start Target Search Loop..."
    #turn true for single picture debuging
    first = False
    
    beagle = NetworkTable.getTable("GRIP")
    goals_table = beagle.getSubTable("aGoalContours")
    
    while True:
	
        #TODO: Fetch image from camera.
        # img = cv2.imread("0.jpg")
        bytes += stream.read(16384)
        b = bytes.rfind('\xff\xd9')
        a = bytes.rfind('\xff\xd8', 0, b-1)
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype = np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            goalFinder.process_image(img)

            goals_table.putValue("centerX", NumberArray.from_list(goalFinder.targetXs))
            goals_table.putValue("centerY", NumberArray.from_list(goalFinder.targetYs))
            goals_table.putValue("width", NumberArray.from_list(goalFinder.targetWidths))
            goals_table.putValue("height", NumberArray.from_list(goalFinder.targetHeights))
            goals_table.putValue("area", NumberArray.from_list(goalFinder.targetAreas))
            
            #Use if you want to the save the image and retrieve it later.
	    if first:
		first = False
	    	cv2.imwrite("test.jpg", img)
	
	goals_table.putNumber("OwlCounter", goals_table.getNumber("OwlCounter", 0) + 1) 

	sleep(.01)


if __name__ == "__main__":
    main()
