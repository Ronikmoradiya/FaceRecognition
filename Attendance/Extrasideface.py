#https://stackoverflow.com/questions/14167886/how-to-detect-front-and-side-view-of-human-face-using-opencv

import tkinter as tk

from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import pymysql.connections
import datetime
import time

#####Window is our Main frame of system
window = tk.Tk()
window.title("Instance It Solutions")

window.geometry('1280x720')
window.configure(background='snow')



def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)
def err_screen():
    Notification.configure(text="fill values", bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)
            

###For take images for datasets
def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            detector_profile = cv2.CascadeClassifier('haarcascade_profileface.xml') #side face
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                face_profile = detector_profile.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    if sampleNum < 25:
                        #print('50')
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #(0,255,0)
                    
                        cv2.putText(img, "Front Face", (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("InstanceIt2_TrainingImage -- 1/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                    
                for (x, y, w, h) in face_profile:
                    if sampleNum < 50:
                        #print('100')
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #(0,255,0)
                    
                        cv2.putText(img, "Left Side Face", (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("InstanceIt2_TrainingImage -- 1/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                
                for (x, y, w, h) in face_profile:
                    if sampleNum<70 or sampleNum==70:
                        #print('150')
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #(0,255,0)
                    
                        cv2.putText(img, "Right Side Face", (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
                    
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("InstanceIt2_TrainingImage -- 1/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('InstaneIt2_TrainingImageLabel -- 1\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()

            try:
                global cursor
                connection = pymysql.connect(host='localhost', user='root', password='', db='InstanceIt2')
                cursor = connection.cursor()
            except Exception as e:
                print(e)

                ####Now enter attendance in Database
            insert_data =  "INSERT INTO user VALUES (%s, %s)"
            VALUES = (str(l1),str(l2))
            try:
                #cursor.execute(sql)  ##for create a table
                cursor.execute(insert_data, VALUES)##For insert data into table
                connection.commit()
            except Exception as ex:
                print(ex)  #

            training()
            print("training done")
            
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=250, y=400)


###for choose subject and fill attendance
def Fillattendances():
        
        now = time.time()  ###For calculate seconds of video
        future = now + 20
        if time.time() < future:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read("InstaneIt2_TrainingImageLabel -- 1\Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notification.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                    Notification.place(x=250, y=400)

                harcascadePath = "haarcascade_frontalface_default.xml"
                harcascadePath_profile = "haarcascade_profileface.xml" #side face
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                faceCascade_profile = cv2.CascadeClassifier(harcascadePath_profile)
                df = pd.read_csv("InstaneIt2_TrainingImageLabel -- 1\StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    faces_profile = faceCascade_profile.detectMultiScale(gray, 1.2, 5)
                    f = [faces,faces_profile]
                    for (x, y, w, h) in faces :
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf < 50):
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            #En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                print(attendance)
                

                ##Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                
                

                ###Connect to the database
                try:
                    global cursor
                    connection = pymysql.connect(host='localhost', user='root', password='', db='InstanceIt2')
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                ####Now enter attendance in Database
                insert_data =  "INSERT INTO attandance VALUES (0, %s, %s, %s,%s)"
                VALUES = (str(Id), str(aa), str(date), str(timeStamp))
                try:
                    #cursor.execute(sql)  ##for create a table
                    cursor.execute(insert_data, VALUES)##For insert data into table
                    connection.commit()
                except Exception as ex:
                    print(ex)  #

                M = "hey, " +aa+ "your Attendance filled Successfully "
                Notification.configure(text=M, bg="Green", fg="white", width=70, font=('times', 15, 'bold'))
                Notification.place(x=250, y=400)

                cam.release()
                cv2.destroyAllWindows()
                



def training():
    #InstanceIt2_TrainingImage -- 1
    #InstaneIt2_TrainingImageLabel -- 1
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector,faces,Id
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:

        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l='please make "InstanceIt2_TrainingImage -- 1" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("InstaneIt2_TrainingImageLabel -- 1\Trainner.yml")
    except Exception as e:
        q='Please make "InstaneIt2_TrainingImageLabel -- 1" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('AMS.ico')


message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System", bg="cyan", fg="black", width=50,
                   height=3, font=('times', 30, 'italic bold '))

message.place(x=80, y=20)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                      height=3, font=('times', 17, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="black", bg="deep pink", font=('times', 15, ' bold '))
lbl.place(x=200, y=200)

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="black", bg="deep pink", font=('times', 15, ' bold '))
lbl.place(x=200, y=200)

txt = tk.Entry(window, validate="key", width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="black", bg="deep pink", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)
clearButton = tk.Button(window, text="Clear",command=clear,fg="black"  ,bg="deep pink"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=210)

clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="black"  ,bg="deep pink"  ,width=10 ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton1.place(x=950, y=310)


txt2 = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
txt2.place(x=550, y=310)


takeImg = tk.Button(window, text="Take Images",command=take_img,fg="white"  ,bg="blue2"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=90, y=500)


FA = tk.Button(window, text="Automatic Attendace",fg="white",command=Fillattendances  ,bg="blue2"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
FA.place(x=690, y=500)


window.mainloop()
