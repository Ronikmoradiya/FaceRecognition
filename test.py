#!C:\Users\DHRUVI SONANI\AppData\Local\Programs\Python\Python37-32\python.exe

print("hi")
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
            #clear()
            #clear1()
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
                    if sampleNum < 41:
                        #print('50')
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #(0,255,0)
                    
                        cv2.putText(img, "Front Face", (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("InstanceIT_WithSideFaceImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
            
                for (x, y, w, h) in face_profile:
                    if sampleNum>=41 and sampleNum < 80:
                        #print('100')
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #(0,255,0)
                        cv2.putText(img, "Left Side Face", (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("InstanceIT_WithSideFaceImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
            
                for (x, y, w, h) in face_profile:
                    if sampleNum<120 and sampleNum==120:
                      
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #(0,255,0)
                        cv2.putText(img, "Right Side Face", (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("InstanceIT_WithSideFaceImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 120:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('InstaceIT_WithSideFaceLabel\StudentDetails.csv', 'a+') as csvFile:
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
                training()
                print("training done")
                res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
                Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
                Notification.place(x=250, y=400)
            except Exception as ex:
                print(ex)
        except FileExistsError as F:
            print(F)
            

###for choose subject and fill attendance
def Fillattendances():
        global recognizer,attendance
        now = time.time()  ###For calculate seconds of video
        future = now + 20
        try:
            global cursor
            connection = pymysql.connect(host='localhost', user='root', password='', db='InstanceIt2')
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        if time.time() < future:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read("InstaceIT_WithSideFaceLabel\Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notification.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                    Notification.place(x=250, y=400)

                harcascadePath = "haarcascade_frontalface_default.xml"
                harcascadePath_profile = "haarcascade_profileface.xml"
                #harcascadePath_profile = "haarcascade_profileface.xml" #side face
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                faceCascade_profile = cv2.CascadeClassifier(harcascadePath_profile)
                df = pd.read_csv("InstaceIT_WithSideFaceLabel\StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                global Id ,gray
                while True:
                    
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    faces_profile = faceCascade_profile.detectMultiScale(gray, 1.2, 5)
                    #f = [faces,faces_profile]
                    for (x, y, w, h) in faces:
                        
                        Id = att(x,y,w,h,im)
                    for (x, y, w, h) in faces_profile:
                       
                        Id = att(x,y,w,h,im)                            
                        
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
                insert_data =  "INSERT INTO attandance VALUES (0, %s, %s, %s,%s)"
                VALUES = (str(give_ID), str(aa), str(date), str(timeStamp))
                M = "hey, " +aa+ " your Attendance filled Successfully "

                ####Now enter attendance in Database
                try:
                    #cursor.execute(sql)  ##for create a table
                    cursor.execute(insert_data, VALUES)##For insert data into table
                    connection.commit()
                except Exception as ex:
                    print(ex)  #

                try:
                    Notification.configure(text=M, bg="Green", fg="white", width=70, font=('times', 15, 'bold'))
                    Notification.place(x=250, y=400)
                except Exception as e:
                    print(" ")

                cam.release()
                cv2.destroyAllWindows()
                

def att(x,y,w,h,im):
                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])    
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        if (conf < 50):
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp,give_ID
                            
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            #aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            get_name = "SELECT Enroll_name FROM user WHERE Er_no = %s"
                            give_ID = str(Id)
                            cursor.execute(get_name,give_ID);
                            aaa = cursor.fetchone();
                            aa = aaa[0]
                            global tt
                            tt = str(Id) + "-" + aa
                            #En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                            
                        else:
                            Id = 'Unknown'
                            aa = 'no name'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)


                        
    

def training():
    global detector,faces,Id,detector_profile
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    detector_profile = cv2.CascadeClassifier("haarcascade_profileface.xml")
    
    try:

        faces, Id = getImagesAndLabels("InstanceIT_WithSideFaceImage")
    except Exception as e:
        l='please make "InstanceIT_WithSideFaceImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("InstaceIT_WithSideFaceLabel\Trainner.yml")
    except Exception as e:
        q='Please make "InstaceIT_WithSideFaceLabel" folder'
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
        faces_profile = detector_profile.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces: # for front faces
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
        for (x, y, w, h) in faces_profile:  #for profile faces
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
