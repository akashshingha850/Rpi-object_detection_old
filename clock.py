import time
import RPi.GPIO as GPIO
import os
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)

#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = 0
while True:
  

  hour = time.strftime("%H")
  hour = int(hour)

  #os.system("date '+%I:%M %P %A %d %B %Y' | festival --tts")

  os.system('echo "It is time for breakfast" | festival --tts')
  print hour
  
  
  
    
  #time.sleep(1)
