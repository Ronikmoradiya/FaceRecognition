#stream = cv2.VideoCapture('http://192.168.1.64:80/videostream.cgi?user=admin&pwd=admin@123')
#stream = cv2.VideoCapture(0)
# Use the next line if your camera has a username and password
#stream = cv2.VideoCapture('rstp://192.168.1.64:554/1')  
#stream = cv2.VideoCapture("rtsp://admin:admin%123@192.168.1.64/axis-media/media.amp")
#stream = cv2.VideoCapture('http://192.168.1.64:8081/')
#admin:admin123@
#stream = cv2.VideoCapture("rtsp://admin:admin@123@{}:525/stream2".format('192.168.1.64'))

import cv2
import numpy
stream = cv2.VideoCapture('rtsp://192.168.1.64:554/')
while True:
    try:
        r,f = stream.read()
        cv2.imshow('IP Camera',f)
    except Exception:
        print("Except")


    if cv2.waitKey(10)&0xFF==ord('q'):
        break
stream.release()
cv2.destroyAllWindows()
