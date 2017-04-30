import numpy as np
import cv2
import curses
import RPi.GPIO as GPIO
import time
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
GPIO.setmode(GPIO.BOARD)
##GPIO.setmode(GPIO.BCM)

GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

TRIG = 16
ECHO = 18
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('apple.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#set GPIO numbering mode and define output pins
def right(x=1000):
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,True)
    GPIO.output(15,False)
    time.sleep(x)
    return;

def left(x=1000):
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(x)
    return;

def up():
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,False)
    GPIO.output(15,True)
    return;

def pause(x=0):
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    time.sleep(x)
    return;
def objdetect():
    t1=time.time()
    cap = cv2.VideoCapture(0)
    count=0
    face_cascade = cv2.CascadeClassifier('apple.xml')
    while 1:
        pause();
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            count+=1
            #print 'detected'
            #print(count)

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

        if(count>=10):
                #print("yes")
            return 1
        if(time.time()-t1>=10):
            return 0
        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def usr():
    GPIO.output(TRIG, False)
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print(distance)
    return distance;

dir="F";
##up();
pause()

# given:
bot_time=time.time();
total_time=10
uni_time=time.time()
while True and time.time()-uni_time<=200:
	dist=usr()
	if (dist<=100 and dir=="F"):
		bot_time=time.time()-bot_time
        pause(1)
        result=objdetect()
        if result==1:
            print("yes, object detected")
            execfile('yes.py')
            break

        elif result==0:
        	if(bot_time>=total_time-4): ##wall
          		print("wall")
            	up()
            	time.sleep(2.99)
            	pause()
            	print("reached near wall")
            	right(0.48)
            	up()
            	time.sleep(1)
            	right(0.48);
            	up();
            	time.sleep(1)
				dir="R"
				bot_time=time.time()
			else: ##some other object
				right(0.48)
				up()
				time.sleep(1)
				left(0.48)
				up()
				time.sleep(1)
				left(0.48)
				up()
				time.sleep(1)
				right(0.48)
				up()
				dir="F"

    elif (dist<=100 and dir=="R"):
		bot_time=time.time()-bot_time
        pause(1)
        result=objdetect()
        if result==1:
            print("yes, object detected")
            execfile('yes.py')
            break

        elif result==0:
        	if(bot_time>=total_time-4): ##wall
            	print ("wall")
            	up()
            	time.sleep(2.99)
            	pause()
            	print ("reached near wall")
            	left(0.48)
            	up()
            	time.sleep(1)
            	left(0.48);
            	up();
            	time.sleep(1)
				dir="F"
				bot_time=time.time()
			else: ##some other object
				left(0.48)
				up()
				time.sleep(1)
				right(0.48)
				up()
				time.sleep(1)
				right(0.48)
				up()
				time.sleep(1)
				left(0.48)
				up()
				dir="R"
    else:
        up();
    # time.sleep(0.1)

pause()

GPIO.cleanup()