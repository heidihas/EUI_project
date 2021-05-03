import cv2
import time
import serial
from multiprocessing.connection import Client

no_face = False
acc_on = False
vibrated = False
sent = False

steps_start = 0
steps_end = 0

th_no_face = 10
th_vib = 30
th_vib_again = 8
start_working = time.time()
vibration_time = time.time()
start = time.time()

face_cascade = cv2.CascadeClassifier('/Users/heidi/Dokumentit/EUI_project/haarcascade_frontalface_default.xml')

video = cv2.VideoCapture(0)

address = ('localhost', 6000)
conn = Client(address)

with serial.Serial('/dev/cu.usbmodem144301', 9600, timeout=1) as ser:
    
    while True:
        check, frame = video.read()
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6, minSize=(200,200))
    
        if len(faces) == 0 and no_face == False:
            no_face = True
            start = time.time()
        elif len(faces) == 0 and no_face == True and acc_on == False and (time.time()-start) > th_no_face:
            #print('start accelerometer')
            acc_on = True
            steps_start = int(ser.readline().decode("utf-8"))
            conn.send('stop')
            sent = True
        elif len(faces) != 0 and no_face == True:
            no_face = False
            start = time.time()
        elif len(faces) != 0 and no_face == False and acc_on == True and (time.time()-start) > th_no_face:
            acc_on = False
            #print('stop accelerometer')
            steps_end = int(ser.readline().decode("utf-8"))
            steps = str(steps_end - steps_start)
            conn.send(steps)
            sent = True
            #print('steps: ', steps)
            #print('total steps: ', steps_total)
            vibrated = False
            start_working = time.time()
    
        if (time.time() - start_working) > th_vib and acc_on == False and vibrated == False:
            #print('vibrate')
            conn.send('vibrate')
            sent = True
            vibrated = True
            vibration_time = time.time()
        elif (time.time() - vibration_time) > th_vib_again and acc_on == False and vibrated == True:
            #print('vibrate again')
            conn.send('vibrate')
            sent = True
            vibration_time = time.time()
        
        if not sent:
            conn.send('empty')
        sent = False
        
        ser.readline()

        for x,y,w,h in faces:
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

        cv2.imshow('Face Detector', frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

video.release()
cv2.destroyAllWindows()