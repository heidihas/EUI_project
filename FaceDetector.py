import cv2
import time
import serial

no_face = False
acc_on = False
vibrated = False
steps_start = 0
steps_end = 0
steps_total = 0
start_working = time.time()
vibration_time = time.time()
start = time.time()
face_cascade = cv2.CascadeClassifier('/Users/hassinh3/Documents/Other_studies/haarcascade_frontalface_default.xml')

video = cv2.VideoCapture(0)

with serial.Serial('/dev/cu.usbmodem141101', 9600, timeout=1) as ser:
    
    while True:
        check, frame = video.read()
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6, minSize=(200,200))
    
        if len(faces) == 0 and no_face == False:
            no_face = True
            start = time.time()
        elif len(faces) == 0 and no_face == True and acc_on == False and (time.time()-start) > 10:
            print('start accelerometer')
            acc_on = True
            steps_start = int(ser.readline().decode("utf-8"))
        elif len(faces) != 0 and no_face == True:
            no_face = False
            start = time.time()
        elif len(faces) != 0 and no_face == False and acc_on == True and (time.time()-start) > 10:
            acc_on = False
            print('stop accelerometer')
            steps_end = int(ser.readline().decode("utf-8"))
            steps_total = steps_total + (steps_end - steps_start)
            print('steps: ', steps_end - steps_start)
            print('total steps: ', steps_total)
            vibrated = False
            start_working = time.time()
    
        if (time.time() - start_working) > 20 and acc_on == False and vibrated == False:
            print('vibrate')
            vibrated = True
            vibration_time = time.time()
        elif (time.time() - vibration_time) > 5 and acc_on == False and vibrated == True:
            print('vibrate again')
            vibration_time = time.time()
        
        ser.readline()

        for x,y,w,h in faces:
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

        cv2.imshow('Face Detector', frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

video.release()
cv2.destroyAllWindows()