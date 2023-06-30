import cv2
import numpy as np
import os
import pandas as pd
import time
import datetime
from datetime import datetime, timedelta
import pymysql.connections
import sqlite3
from datetime import date

stream = cv2.VideoCapture('rtsp://192.168.1.64:554/')
print("Streamed")
global aa,tt,cursor,connection,NewTime,compareTime  
try:
    connection = pymysql.connect(host='localhost', user='root', password='', db='InstanceIt2')
    cursor = connection.cursor()
except Exception as e:
    print(e)

harcascadePath = "haarcascade_frontalface_default.xml"
harcascadePath_profile = "haarcascade_profileface.xml"
faceCascade = cv2.CascadeClassifier(harcascadePath)
faceCascade_profile = cv2.CascadeClassifier(harcascadePath_profile)
font = cv2.FONT_HERSHEY_SIMPLEX
FMT = '%H:%M:%S'
      
while True:

    try :
        def add_database(insert_data,VALUES):
            cursor.execute(insert_data, VALUES)##For insert data into table
            connection.commit()
        
        def att():
                cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

                # Recognize the face belongs to which ID
                Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])  #Our trained modelr is working here
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                # retrieve name
                get_name = "SELECT Enroll_name FROM user WHERE Er_no = %s"
                give_ID = str(Id)
                cursor.execute(get_name,give_ID);
                aaa = cursor.fetchone();
                try:
                    
                    print("Name Retrived :  <<<<<<<<<"+str(aaa[0]))
                    # Set rectangle around face and name    of the person
                    cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                    if(confidence < 50):

                        cv2.putText(im, str(Id) + "-" +str(aaa[0])+"-"+str(confidence), (x,y-40), font, 1, (255,255,255), 3)
                    else:
                        cv2.putText(im, str(confidence), (x,y-40), font, 1, (255,255,255), 3)
                    

                    takeTime = "SELECT Time,Date,Er_no FROM attandance WHERE Er_no = %s ORDER BY Sr_no DESC"
                    takeEr_no = str(Id)
                    cursor.execute(takeTime,takeEr_no)
                
                    
                    exeTime = cursor.fetchone()
                    if (cursor.rowcount > 0 and exeTime[2]==str(Id)):
                        abc = (datetime.strptime(exeTime[0],FMT) + timedelta(minutes=2)).time()
                        
                    select_data = "SELECT Er_no FROM attandance WHERE Er_no=%s"
                    VALUES_insert = (str(Id))
                    
                    insert_data =  "INSERT INTO attandance VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(Id), str(aaa[0]), str(date), str(timeStamp))
                    if(cursor.execute(select_data,VALUES_insert) == 0):
                        add_database(insert_data,VALUES)
                        
                    else :
                        try:
                            if(cursor.rowcount == 0):
                                add_database(insert_data,VALUES)
                            elif (abc < datetime.strptime(timeStamp,FMT).time() ) :
                                add_database(insert_data,VALUES)
                            elif(exeTime[1]<today):
                                add_database(insert_data,VALUES)
                            else :
                                pass 
                        except Exception as ex:
                            print(ex)  #
                except TypeError:
                    print(">>>>>>>>>> No Name <<<<<<<")

        today = date.today()
        
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
        try:
            recognizer.read("InstaceIT_WithSideFaceLabel\Trainner_final.yml")
        except:
            e = 'Model not found,Please train model'
        
    
        
        # Looping starts here
        while True:

            ret, im =stream.read()
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2,5) #default
            faces_profile = faceCascade_profile.detectMultiScale(gray, 1.2,5) #default
            flipped = cv2.flip(gray, 1)
            faces_profile_right = faceCascade_profile.detectMultiScale(flipped, 1.3, 5)

            
            for(x,y,w,h) in faces:
                att()
            for(x,y,w,h) in faces_profile:
                att()
            for(x,y,w,h) in faces_profile_right:
                att()

            cv2.imshow('IP Camera',im)    
            # press q to close the program
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
        # Terminate video
        stream.release()

        # Close all windows
        cv2.destroyAllWindows()        
    except Exception:
        print("Except")

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()
