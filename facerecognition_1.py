##########################################
import os
import tkinter
import face_recognition
import cv2
import numpy as np
import csv
from tkinter import *
import cvzone
##########################################
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
###########################################
from datetime import *
import pickle
from PIL import Image, ImageTk
import time
import os
###########################################


root = Tk()
Captures=[]
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
def showattendance():
    try:
        Label(root, text="PRESENT :-", font=('algerian', 14)).place(x=700, y=240)
        Label(root, text=Captures[0]['Name'],font=('algerian',14),border=10).place(x=700,y=280,width=500)
        Label(root, text=Captures[0]['Rollno'], font=('algerian', 14), border=10).place(x=700, y=320, width=500)
    except:
        Label(root, text="USER NOT FOUND", font=('algerian', 14)).place(x=700, y=240)
def Close():
    video_capture.release()
    cv2.destroyAllWindows()
    f.close()
    root.destroy()

def openexcel():
    Close()
    filename=f'{current_date}.csv'
    if os.name=='nt':
        os.system(f'start {filename}')


root.geometry("1300x600")
root.title("Face Attendance System")
# root.configure(bg="magneta2")


Label(root, text="BRACT's", font=("Algerian", 22, "bold"), bg="white", fg="black").pack()
Label(root, text="Vishwakarma Institute of Information Technology", font=("Algerian", 36, "bold"), bg="white", fg="black").pack()
Label(root, text="***************************************************************************************************", font=("Algerian", 14, "bold"), bg="white", fg="black").pack()
Label(root, text="ATTENDANCE SYSTEM", font=("Algerian", 22, "bold"), bg="white", fg="black").pack()
f1 = LabelFrame(root, bg="white")
f1.pack(anchor='nw')
L1 = Label(f1, bg="blue")
L1.pack()

b1=Button(root,text="OPEN EXCEL FILE",font=('algerian',14),bg='dark violet',fg='black',command=openexcel)
b1.place(x=700,y=180)
b6=Button(root,text="close",font=('algerian',14),bg='dark violet',fg='black',command=Close)
b6.place(x=1000,y=180)




print("Loading Encoded file .......")
file = open('encoding.py', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
known_face_encodings, known_face_names = encodeListKnownWithIds
# print(studentIds)
print("Encoded file Loaded successfully ")





cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-a92d4-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-a92d4.appspot.com"
})

bucket = storage.bucket()




# print(known_face_encodings)
video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# List of expected students
students = known_face_names.copy()

face_locations = []
face_encodings = []


f = open(f"{current_date}.csv", "w+", newline="")
lnwter=csv.writer(f)

while True:
    ret, frame = video_capture.read()
    imgs = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgs = ImageTk.PhotoImage(Image.fromarray(imgs))
    L1['image'] = imgs

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)


    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


    for face_encoding in face_encodings:
        for faceloc in face_locations:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)



        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print(known_face_names[best_match_index])
            studentInfo = db.reference(f'Student/{name}').get()
            # print(studentInfo)
            Captures=[studentInfo]
            showattendance()


            if name in students:
                students.remove(name)
                current_time = time.strftime("%H:%M:%S")
                lnwter.writerow([studentInfo['Name'],studentInfo['Batch'],studentInfo['Rollno'],studentInfo['PRN No'], current_time])


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    root.update()


video_capture.release()
cv2.destroyAllWindows()
f.close()
