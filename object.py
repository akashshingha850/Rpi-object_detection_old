#Libraries
import RPi.GPIO as GPIO
import time
import os

from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input, decode_predictions
import numpy as np
import sys, os, time, subprocess, pickle
from googletrans import Translator


 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_TRIGGER2 = 20
GPIO_ECHO2 = 16
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

os.system("./start_stream.sh")

model = MobileNet(weights='imagenet')
devnull = open('os.devnull', 'w')
ipaddr = subprocess.check_output(["hostname", "-I"]).decode("utf-8").strip()
commd = "http://"+ipaddr+":9000/?action=snapshot"
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


def distance2():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER2, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER2, False)
 
    StartTime2 = time.time()
    StopTime2 = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime2 = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime2 = time.time()
 
    # time difference between start and arrival
    TimeElapsed2 = StopTime2 - StartTime2
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance2 = (TimeElapsed2 * 34300) / 2
 
    return distance2

 
if __name__ == '__main__':
    try:
        while True:
            os.system("rm lookdave.wav")
            dist = distance()
            dist2 = distance2()

            print ("front = %f cm" % dist)
            print ("down = %f cm" % dist2)
            time.sleep(2)



            if(dist2 > 200):
                print ("Measured Distance = %f cm" % dist2)
                os.system("pico2wave -w lookdave.wav ' A hole in front of 2 meters' && aplay lookdave.wav")
                os.system("rm lookdave.wav")
                time.sleep(3)

                
            if(dist <300 and dist > 250):
                print ("Measured Distance = %f cm" % dist)
                os.system("pico2wave -w lookdave.wav ' A object in front of three meters' && aplay lookdave.wav")
                os.system("rm lookdave.wav")
                #time.sleep(5)

            if(dist <250 and dist > 200):
                print ("Measured Distance = %f cm" % dist)
                os.system("pico2wave -w lookdave.wav ' A object in front of two and a half meters' && aplay lookdave.wav")
                os.system("rm lookdave.wav")
                #time.sleep(5)

            if(dist <200 and dist > 150):
                print ("Measured Distance = %f cm" % dist)
                os.system("pico2wave -w lookdave.wav ' A object in front of two meters' && aplay lookdave.wav")
                os.system("rm lookdave.wav")
                #time.sleep(5)

            if(dist <150 and dist > 100):
                print ("Measured Distance = %f cm" % dist)
                os.system("pico2wave -w lookdave.wav ' A object in front of one and a half meters' && aplay lookdave.wav")
                os.system("rm lookdave.wav")
                #time.sleep(5)
                
            if(dist <100 and dist > 50):
                print ("Measured Distance = %f cm" % dist)
                os.system("pico2wave -w lookdave.wav ' A object in front of one meter' && aplay lookdave.wav")
                os.system("rm lookdave.wav")
                 

            if(dist <50 and dist > 0):
                print ("Measured Distance = %f cm" % dist)
                os.system("pico2wave -w lookdave.wav ' A object in front of half meter' && aplay lookdave.wav")
                os.system("rm lookdave.wav")
                #time.sleep(5)
                
            if(dist <300 and dist > 0):
                subprocess.run(["wget", "-O", "photo.jpg", commd], stdout=devnull, stderr=subprocess.STDOUT)

                img_path = 'photo.jpg'
                img = image.load_img(img_path, target_size=(224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)

                preds = model.predict(x)
                print('Predicted:', decode_predictions(preds, top=3)[0])
                recognize = decode_predictions(preds)
                speak = "This is a " + recognize[0][0][1]
                subprocess.check_output(["espeak", "-k5", "-s150", speak])
                print('------------------------')                 
            
        time.sleep(3)
        
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
