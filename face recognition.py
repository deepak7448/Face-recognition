import cv2
import numpy as np
import face_recognition as fe
import os
# import pyttsx3 as textSpeach
from datetime import  datetime
import database as db

# engine = textSpeach.init()
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# # print (rate)                        #printing current voice rate
# engine.setProperty('rate', 155)  
# """VOICE"""
# voices = engine.getProperty('voices')       #getting details of current voice
# #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[2].id)   

image_path = 'img'
EmployeeIMG = []
EmployeeName = []
imgEncodings = []
isExist = os.path.exists(image_path)

if not isExist:
    os.makedirs(image_path)
allimg = os.listdir(image_path)
# print(img)
for employee in allimg:
    # print(employee)
    employee1 = cv2.imread(f'{image_path}/{employee}')
    EmployeeIMG.append(employee1)
    EmployeeName.append(os.path.splitext(employee)[0])
# print(EmployeeName)

def face_Encoding(images) :
    for img in images :
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = fe.face_encodings(img)[0]
        imgEncodings.append(encodeimg)
    return imgEncodings

face = face_Encoding(EmployeeIMG)

camera = cv2.VideoCapture(0)
while True :
    success, frame = camera.read()
    Smaller_frames = cv2.resize(frame, (0,0), None, 0.25, 0.25)

    facesInFrame = fe.face_locations(Smaller_frames)
    encodeFacesInFrame = fe.face_encodings(Smaller_frames, facesInFrame)

    for encodeFace, faceloc in zip(encodeFacesInFrame, facesInFrame):

        matches = fe.compare_faces(face, encodeFace)
        # name = "Unknown"
        facedis = fe.face_distance(face, encodeFace)
        # print(facedis)
        try:
            matchIndex = np.argmin(facedis)
        except:
            pass
        # print(matchIndex)
        try:
            if matches[matchIndex] :
                name = EmployeeName[matchIndex]
                # print(name)
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2-25), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                # print(name)
                db.present(name)
                # print(db.present(name))
                # print(name)                     
                # statment = str('Good morning' + name + 'have a nice day.')
                # engine.say(statment)
                # engine.runAndWait()

            else:
                name="unknown"
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 252), 2)
                cv2.rectangle(frame, (x1, y2-25), (x2, y2), (0, 0, 204), cv2.FILLED)
                cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (249,249,249), 2)
        except:
            name="unknown"
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 252), 2)
            cv2.rectangle(frame, (x1, y2-25), (x2, y2), (0, 0, 204), cv2.FILLED)
            cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (249,249,249), 2)
    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
    # cv2.waitKey(1)