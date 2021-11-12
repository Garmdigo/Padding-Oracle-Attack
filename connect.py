import socket
from binascii import unhexlify, hexlify
import base64
from itertools import cycle
from math import floor
import math

def GetInfo(Cipher):
    C = Cipher.split("\\n")[1].split("\\n")
    iv =   Cipher.split("IV")[1].split("'")
    CipherText = C[0].replace(" ","")
    IV = iv[1].replace("'","")
    return CipherText,IV

def splitBlocks(message):
    Size = len(message)
    Slices = []
    Increment =int(Size/32)
    for i in range(Increment):
        Slices.append(message[i*32:(i+1)*32])
    return Slices

def sliceBlocks(message):
    size = len(message)
    slices = []
    x = 0
    y = 32
    v = size % 32    
    for i in range(size / 32):
       slices.append(message[x:y])
       x += 32
       y += 32
    if(v!=0):
      slices.append(message[x:y])

    return slices

def xor(arg1,arg2):
    return hexlify(''.join(chr(ord(a) ^ ord(b)) for a, b in zip(unhexlify(arg1), unhexlify(arg2))))


def requestServer(prefix):
    r.send(("-e " + str(prefix)).encode())     # Encryption of the secret message
    x = r.recv(1024).decode()
    return x
def checkValidate(Ciphertext, IV):
    r.send(("-V " + str(Ciphertext) + " " + str(IV)).encode())     # Encryption of the secret message
    x = r.recv(1024).decode()
    return x

def listToString(input):
    str=""
    for i in range(len(input)):
       str = str + input[i]
    return str

def getNtoLast(bytes,position):
    return bytes[-positon]
def LastNbyte(bytes,getNtoLast,choosebyte):
    LastBlock = getNtoLast(bytes,getNtoLast)
    return LastBlock[-choosebyte:]

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("128.186.120.191", 31337))






#r.send("-e".encode())     # Encryption of the secret message
#x = r.recv(1024).decode()
#r.send("-e".encode())
#y = r.recv(1024).decode()
x = requestServer('')

Ciphertext, IV = GetInfo(x)
#CT2, IV2 = GetInfo(y)
CTencode = bytes(Ciphertext)
#CT = bytes(CT2)

d = sliceBlocks(Ciphertext)
b=d[0]
d[-1]=b
a= d[-1]
c = xor(d[0], IV)


str = listToString(d)
#print(str[0])
#u = bytearray(str, 'latin-1')
#nIV = bytearray(IV, 'latin-1')
#print(type(u))
#z = checkValidate(u, nIV)
#print(z)
print(a[-2])
print(d)
print(IV)
print(Ciphertext)
print(c)

#r.send("-e abcdef0123456789".encode()) # Encryption of abcdef0123456789 || message
#x = r.recv(1024).decode()
#print x.replace(" ", "")


#p = checkValidate(d.decode(), IV)
#print(p)


#r.send("-V 6a9215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810 659a4a7cf4273befce277e5336202d69".encode()) # Valid ciphertext and IV
#z = r.recv(1024).decode()
#print z

#y = checkValidate('6a9215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810', '659a4a7cf4273befce277e5336202d69')
#print y

#r.send("-V 6a96a9215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810 659a4a7cf4273befce277e5336202d69215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810 659a4a7cf4273befce277e5336202d6a".encode()) # Invalid (flipped IV bit)
#x = r.recv(1024).decode()
#print x




r.close()
