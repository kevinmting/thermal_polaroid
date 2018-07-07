import RPi.GPIO as GPIO
import time
from subprocess import call
from Adafruit_Thermal import *
from PIL import Image
import pdb
import signal

def main():
    #CONSTANTS
    TRIGGER_PIN = 4
    #PICTURE_PATH = "TEST.BMP"
    PICTURE_PATH = "/home/pi/tmp.jpg"
    PRINTER_WIDTH = 384
    PRINTER_HEIGHT = 384
    LED_PIN = 25

    #SETUP
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.setup(LED_PIN, GPIO.OUT)

    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

    fastcamdir = '/home/pi/src/rasperry-pi-userland/host_applications/linux/apps/raspicam/raspifastcamd_scripts/'
    call(["sh", "start_camd.sh"])

    for i in range(4):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.2)
    GPIO.output(LED_PIN, GPIO.HIGH)

    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        input_state = GPIO.input(TRIGGER_PIN)
        if input_state == False:
            
            print('Button pressed')
            
            print "capturing image"
            #call(["raspistill","-v","-n","-o",PICTURE_PATH])
            call(["sh", "do_caputure.sh"])
            time.sleep(1)
            
            input_state = GPIO.input(TRIGGER_PIN)
            if input_state == False:
                print('SHUTTING DOWN')
                call(["sh", "stop_camd.sh"])    
                for i in range(4):
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    time.sleep(0.2)
                    GPIO.output(LED_PIN, GPIO.LOW)
                    time.sleep(0.2)    
                #call(["sudo", "poweroff"])
            else:
                do_print = True
                if do_print:
                    time.sleep(0.5)
                    print "printing image"
                    im = Image.open(PICTURE_PATH)
                    scaled = im.resize((PRINTER_WIDTH, PRINTER_HEIGHT))
                    
                    #call(["lp","-o","fit-to-page","-c","test.bmp"])
                    printer.printImage(scaled, LaaT=True)

                    GPIO.output(LED_PIN, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(LED_PIN, GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    #pdb.set_trace()
                    
                    #add blank prints so image is fully out of the printer
                    printer.println("")
                    printer.println("")
                    printer.println("")

                    time.sleep(5)
     
#

def sigint_handler(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    print("Stop pressing ctrl+c!")
    call(["sh", "stop_camd.sh"])
    sys.exit(1)
    
    # restore the handler here. 
    signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, sigint_handler)
    main()