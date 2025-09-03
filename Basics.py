import cv2
import numpy as np
import face_recognition

# loading images and converting them into rgb values
imgElon = face_recognition.load_image_file("ImagesBasics/Elon_Musk_Royal_Society.webp")
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)

imgTest = face_recognition.load_image_file("ImagesBasics/elon-musk-test.jpg")
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

imgBill = face_recognition.load_image_file("ImagesBasics/bill-gates.jpeg")
imgBill = cv2.cvtColor(imgBill, cv2.COLOR_BGR2RGB)

# finding faces from images and their encodings

faceLoc = face_recognition.face_locations(imgElon)[0]
encodeElon = face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]), (255,0,255), 2)

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]), (255,0,255), 2)

faceLocBill = face_recognition.face_locations(imgBill)[0]
encodeBill = face_recognition.face_encodings(imgBill)[0]
cv2.rectangle(imgBill,(faceLocBill[3],faceLocBill[0]),(faceLocBill[1],faceLocBill[2]), (255,0,255), 2)


# comparing faces and seeing their 'similarity'
    # elon w elon
results = face_recognition.compare_faces([encodeElon], encodeTest)


    # elon w bill
otherRes = face_recognition.compare_faces([encodeElon], encodeBill)


# finding similarity between images
faceDis = face_recognition.face_distance([encodeElon], encodeTest) 
faceDisBE = face_recognition.face_distance([encodeBill], encodeTest) 
print(results, faceDis)
print(otherRes, faceDisBE)

cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50,50), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
cv2.putText(imgBill, f'{otherRes} {round(faceDisBE[0], 2)}', (50,50), cv2.FONT_HERSHEY_COMPLEX,.6,(0,0,255),1)

cv2.imshow('Elon Musk', imgElon)
cv2.imshow('Elon Test', imgTest)
cv2.imshow('Bill Gates', imgBill)

cv2.waitKey(0)



