import socket
import sys


HOST = '127.0.0.1'
PORT = 10000
s = socket.socket()
s.connect((HOST, PORT))

print s

while 1:
    msg = raw_input("Command To Send: ")
    if msg == "close":
       s.close()
       sys.exit(0)
    s.send(msg)