import RPi.GPIO as GPIO
import time
from subprocess import call

TRIGGER_PIN = 4
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(TRIGGER_PIN)
    if input_state == False:
        print('Button pressed')
        
        print "capturing image"
        call(["raspistill","-v","-n","-o","test.bmp"])
        
        print "printing image"
        call(["lp","-o","fit-to-page","-c","test.bmp"])
        
        time.sleep(0.2)