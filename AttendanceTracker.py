import cv2
import numpy as np
import face_recognition
import os

# generate a list of encodings for all the students in a class using their picture
PATH = 'ImagesStudents'
VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}  # NEW

images = []
studentNames = []
myList = os.listdir(PATH)

for student in myList:
    name, extension = os.path.splitext(student)
    
    if extension.lower() not in VALID_EXTS:
        continue
    
    currImg = cv2.imread(f'{PATH}/{student}')
    if currImg is None:
        print(f"[WARN] Could not read: {PATH}/{student}")
        continue
    
    images.append(currImg)
    studentNames.append(os.path.splitext(student)[0])
    
print(studentNames)


# function to turn images into their encodings
def getEncodings(images):
    encodedList = []
    for index, img in enumerate(images):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodedImg = face_recognition.face_encodings(img)
        
        if not encodedImg:
            print(f"[WARN] No face detected in image #{index}. Skpping.")
            continue
        encodedImg = encodedImg[0]
        encodedList.append(encodedImg)
    
    return encodedList

def markAttendance(name):
    pass

print("Beginning Encoding")
encodeListKnownFaces = getEncodings(images)
print("Encoding Complete")

# find encodings matching with live camera
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    capture.release()
    capture = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    
if not capture.isOpened():
    raise SystemExit("[ERROR] Could not open camera. Try a different index (1/2) or check app permissions (System Settings → Privacy & Security → Camera).")

while True:
    success, img = capture.read()
    
    if not success or img is None:
        print("[WARN] Empty frame from camera; skipping this iteration.")
        continue
    
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    facesInFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, facesInFrame)
    
    for encodedFace, faceLocation in zip(encodeCurrFrame, facesInFrame):
        matches = face_recognition.compare_faces(encodeListKnownFaces, encodedFace)
        faceDistance = face_recognition.face_distance(encodeListKnownFaces, encodedFace)
        print(faceDistance)
        matchIndex = np.argmin(faceDistance)
        
        if matches[matchIndex]:
            name = studentNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceLocation
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2), (0,255,0), 2)
            cv2.rectangle(img, (x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
    
