import RPi.GPIO as GPIO
import time
from subprocess import call
from Adafruit_Thermal import *
from PIL import Image
import pdb

#CONSTANTS
TRIGGER_PIN = 4
PICTURE_PATH = "TEST.BMP"
PRINTER_WIDTH = 384
PRINTER_HEIGHT = 384

#SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)



while True:
    input_state = GPIO.input(TRIGGER_PIN)
    if input_state == False:
        print('Button pressed')
        
        print "capturing image"
        call(["raspistill","-v","-n","-o",PICTURE_PATH])
        
        print "printing image"
        im = Image.open(PICTURE_PATH)
        scaled = im.resize((PRINTER_WIDTH, PRINTER_HEIGHT))
        
        #call(["lp","-o","fit-to-page","-c","test.bmp"])
        printer.printImage(scaled, LaaT=True)
        
        pdb.set_trace()
        
        #add blank prints so image is fully out of the printer
        printer.println("")
        printer.println("")
        printer.println("")

        time.sleep(0.2)