#!/usr/bin/python3           # This is client.py file

import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("128.186.120.191", 31337))

try:
    while True:
        data = input()
        s.send(data.encode())
        print (s.recv(1024).decode())

except KeyboardInterrupt:
    s.close()
