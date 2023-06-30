##Author:Amartya Kalapahar
##Project: Absolute Face Technologies Internship Assignment

# We will import openCV library for image processing, opening the webcam etc
#Os is required for managing files like directories
#Numpy is basically used for matrix operations
#PIL is Python Image Library
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

def att():
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

        # Recognize the face belongs to which ID
        Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])  #Our trained modelr is working here
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            

        # retrieve name
        
        #aa = df.loc[df['Enrollment'] == Id]['Name'].values
        # Set the name according to id
        get_name = "SELECT Enroll_name FROM user WHERE Er_no = %s"
        give_ID = str(Id)
        cursor.execute(get_name,give_ID);
        aaa = cursor.fetchone();
        try:
            aa = aaa[0]
            print("Name Retrived :  <<<<<<<<<"+str(aa))
            # Set rectangle around face and name    of the person
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
            if(confidence < 50):

                cv2.putText(im, str(Id) + "-" +str(aa)+"-"+str(confidence), (x,y-40), font, 1, (255,255,255), 3)
            else:
                cv2.putText(im, str(confidence), (x,y-40), font, 1, (255,255,255), 3)
            count = 1

            global NewTime,compareTime  

            takeTime = "SELECT Time,Date,Er_no FROM attandance WHERE Er_no = %s ORDER BY Sr_no DESC"
            
            takeEr_no = str(Id)
            cursor.execute(takeTime,takeEr_no)
            
                #exeTime = datetime.datetime.strftime(convertTuple(exeTime), '%H:%M:%S')
            FMT = '%H:%M:%S'
            exeTime = cursor.fetchone()
            #today1 = date.today()
            if (cursor.rowcount > 0 and exeTime[2]==str(Id)):   
                
                print("got time : " +str(exeTime))
                    #exeTime = convertTuple(exeTime)
                print("Got time1 : "+exeTime[0])
                print("Got Date : "+str(exeTime[1]))
                print("Got Er_no : "+exeTime[2])
                print("to add time")
                abc = (datetime.strptime(exeTime[0],FMT) + timedelta(minutes=2)).time()
                print(abc)
            
                
            select_data = "SELECT Er_no FROM attandance WHERE Er_no=%s"
            VALUES_insert = (str(Id))
            
            insert_data =  "INSERT INTO attandance VALUES (0, %s, %s, %s,%s)"
            VALUES = (str(Id), str(aa), str(date), str(timeStamp))
            if(cursor.execute(select_data,VALUES_insert) == 0):
                print(">>>>>>>>>>>>.First Time Add :: <<<<<<<<<<<<<<<")
                cursor.execute(insert_data, VALUES)##For insert data into table
                connection.commit()
                
            else :
            

                try:
                    
                    print("timestamp : " + str(datetime.strptime(timeStamp,FMT).time()))
                    if(cursor.rowcount == 0):
                        cursor.execute(insert_data, VALUES)##For insert data into table
                        connection.commit()
                    elif (abc < datetime.strptime(timeStamp,FMT).time() ) :
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>added Er no "+ str(Id)+" Name : "+ str(aa))
                        cursor.execute(insert_data, VALUES)##For insert data into table
                        connection.commit()
                    elif(exeTime[1]<today):
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>added Er no "+ str(Id)+" Name : "+ str(aa))
                        cursor.execute(insert_data, VALUES)##For insert data into table
                        connection.commit()
                    else :
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>not added Er no "+ str(Id)+" Name : "+ str(aa))
                     #pass 
                except Exception as ex:
                    print(ex)  #
        except TypeError:
            print(">>>>>>>>>> No Name <<<<<<<")
        


today = date.today()
print("Today's date:", today)

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str
#Method for checking existence of path i.e the directory
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

#assure_path_exists("saved_model/")
#assure_path_exists("C:/Users/DHRUVI SONANI/Downloads/Attendace_management_system-master/saved_model/")

# Load the  saved pre trained mode
#recognizer.read('saved_model/s_model.yml')

recognizer.read('C:/xampp/htdocs/Attendace_management_system-master/InstaceIT_WithSideFaceLabel/Trainner_final.yml')


#recognizer.read('F:/7th sem/face-recognition-assignment-master/s_model.yml')

# Load prebuilt classifier for Frontal Face detection
#cascadePath = "haarcascade_frontalface_default.xml"
#cascadePath_profile = "haarcascade_profileface.xml"

# Create classifier from prebuilt model
#faceCascade = cv2.CascadeClassifier(cascadePath);
#faceCascade_profile = cv2.CascadeClassifier(cascadePath_profile);
# font style
font = cv2.FONT_HERSHEY_SIMPLEX
global aa,tt

# Initialize and start the video frame capture from webcam
#cam = cv2.VideoCapture(0)

recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
try:
    recognizer.read("InstaceIT_WithSideFaceLabel\Trainner_final.yml")
except:
    e = 'Model not found,Please train model'
  #  Notification.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
   # Notification.place(x=250, y=400)

harcascadePath = "haarcascade_frontalface_default.xml"
harcascadePath_profile = "haarcascade_profileface.xml"
faceCascade = cv2.CascadeClassifier(harcascadePath)
faceCascade_profile = cv2.CascadeClassifier(harcascadePath_profile)
#df = pd.read_csv("InstaneIt2_TrainingImageLabel -- 1\StudentDetails.csv")
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
try:
    global cursor
    connection = pymysql.connect(host='localhost', user='root', password='', db='InstanceIt2')
    cursor = connection.cursor()
except Exception as e:
    print(e)

# Looping starts here
while True:
    # Read the video frame
    ret, im =cam.read()

    # Convert the captured frame into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Getting all faces from the video frame
    faces = faceCascade.detectMultiScale(gray, 1.2,5) #default
    faces_profile = faceCascade_profile.detectMultiScale(gray, 1.2,5) #default
    # For each face in faces, we will start predicting using pre trained model
    flipped = cv2.flip(gray, 1)
    faces_profile_right = faceCascade_profile.detectMultiScale(flipped, 1.3, 5)
  
                
    for(x,y,w,h) in faces:
        att()
    for(x,y,w,h) in faces_profile:
        att()
    for(x,y,w,h) in faces_profile_right:
        att()
        
    # Display the video frame with the bounded rectangle
    cv2.imshow('im',im)    
    # press q to close the program
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Terminate video
cam.release()

# Close all windows
cv2.destroyAllWindows()
