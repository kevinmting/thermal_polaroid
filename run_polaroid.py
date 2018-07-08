import RPi.GPIO as GPIO
import time
from subprocess import call
from Adafruit_Thermal import *
from PIL import Image
import pdb
import signal
import os
import socket
import sys
import subprocess

daemon_process = None
client_socket = None

def main():
    #CONSTANTS
    TRIGGER_PIN = 4
    #PICTURE_PATH = "TEST.BMP"
    #PICTURE_PATH = "/home/pi/tmp.jpg"
    PICTURE_PATH = '/home/pi/src/polaroid/picam_pics/polaroid_pic.jpg'
    PRINTER_WIDTH = 384
    PRINTER_HEIGHT = 384
    LED_PIN = 25

        
    #GPIO SETUP
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.setup(LED_PIN, GPIO.OUT)

    #PRINTER SETUP
    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)


    #CAMERA DAEMON SETUP
    global daemon_process
    daemon_process = subprocess.Popen(['python','picam-daemon.py'])
    #call(["python","picam-daemon.py"])
    time.sleep(0.5)

    #CAMERA CLIENT SETUP
    HOST = '127.0.0.1'
    PORT = 10000
    global client_socket
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    print "socket details:\n"
    print client_socket

    #fastcamdir = '/home/pi/src/rasperry-pi-userland/host_applications/linux/apps/raspicam/raspifastcamd_scripts/'
    #call(["sh", "start_camd.sh"])

    blink_led(LED_PIN, 10, 0.2)

    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        input_state = GPIO.input(TRIGGER_PIN)
        if input_state == False:
            
            #try:
            #    call(["rm", PICTURE_PATH])
            #    print("Successfully deleted " + PICTURE_PATH)
            #except:
            #    print("Could not delete " + PICTURE_PATH)
            #print('Button pressed')

            blink_led(LED_PIN, 2, 0.2)

            print "capturing image"
            #call(["raspistill","-v","-n","-o",PICTURE_PATH])
            #call(["sh", "do_caputure.sh"])
            client_socket.send("snap")

            #check if user did a long press --> if so power off
            time.sleep(1)
            input_state = GPIO.input(TRIGGER_PIN)
            if input_state == False:
                exit_gracefully()
                #call(["sh", "stop_camd.sh"])    
                blink_led(LED_PIN, 4, 0.2)    
                call(["sudo", "poweroff"])
            else:
                do_print = True
                if do_print:
                    time.sleep(0.5)
                    print "printing image"
                    im = Image.open(PICTURE_PATH)
                    scaled = im.resize((PRINTER_WIDTH, PRINTER_HEIGHT))
                    
                    #call(["lp","-o","fit-to-page","-c","test.bmp"])
                    printer.printImage(scaled, LaaT=True)
                    
                    
                    #pdb.set_trace()
                    
                    #add blank prints so image is fully out of the printer
                    printer.println("")
                    printer.println("")
                    printer.println("")

                    blink_led(LED_PIN, 3, 0.5)
                    #time.sleep(5)
     
#
def blink_led(LED_PIN, n_times, t_sec):
    for i in range(n_times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(t_sec)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(t_sec)    

def sigint_handler(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    print("Stop pressing ctrl+c!")
    #call(["sh", "stop_camd.sh"])
    exit_gracefully()
    sys.exit(1)
    
    # restore the handler here. 
    signal.signal(signal.SIGINT, sigint_handler)

def exit_gracefully():
    print "shutting down gracefully"

    daemon_process.kill()
    print "successfully killed camera daemon process"

    client_socket.close()
    print "succesfully closed camera client socket"

    print "done shutting down gracefully"


if __name__ == "__main__":
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, sigint_handler)
    
    #change current working directory to directory of python file we are calling
    pathname = os.path.dirname(sys.argv[0])
    fullpath = os.path.abspath(pathname)
    os.chdir(fullpath)
    
    main()
o
