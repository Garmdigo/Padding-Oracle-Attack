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



def sliceBlocks(message):
    size = len(message) /2
    Bytes = message
    slices = []
    x = 0
    y = 32
    v = size % 32
    if(v):
        iter = floor(len(message)/32)
        tmp = []
        for i in range(iter):
           slices.append(message[x:y+1])
           x += 32
           y += 32
        slices.append(message[x:].zfill(32))
        v = 0
    if (v ==0 ):
        pass
    if(v!=0):
      run = True 
      loopcounter = size
      begposition = 0
      endPosition = 32
      while run:
          if(loopcounter > 32):

              slices.append(message[begposition:endPosition+1])

              begposition +=32
              endPosition += 32         
              loopcounter -= 32
          if (loopcounter < 32):
                
                padLength = 32 - loopcounter
                beforePadding = message[begposition:]
                slices.append(message.zfill(padLength))
                print(beforePadding.zfill(padLength))
                run = False
                v = 0
    return slices

def xor(arg1,arg2):
    print(arg1,arg2)
    if( len(arg1) % 2 ==0 & len(arg2) % 2 ==0):
        return hexlify(''.join(chr(ord(a) ^ ord(b)) for a, b in zip(unhexlify(arg1), cycle(unhexlify(arg2)))))
    if (len(arg1) %2 !=0  & len(arg2) % 2 != 0):
        arg1 = unhexlify('0%x' % arg1)
        arg2 = unhexlify('0%x' % arg2)
        return hexlify(''.join(chr(ord(a) ^ ord(b)) for a, b in zip(arg1, cycle(arg2))))

    if ( len(arg2) %2 == 0 & len(arg1) %2 != 0):
        arg1 = unhexlify('0%x' % n)
        return hexlify(''.join(chr(ord(a) ^ ord(b)) for a, b in zip(arg1, cycle(unhexlify(arg2)))))
    
    if ( len(arg1) %2 == 0 & len(arg2) %2 != 0):
        arg2 = unhexlify('0%x' % n)
        return hexlify(''.join(chr(ord(a) ^ ord(b)) for a, b in zip(unhexlify(arg1), cycle(arg2))))

  


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
    return listToString(bytes[-positon])
def LastNbyte(bytes,getNtoLast,choosebyte):
    LastBlock = getNtoLast(bytes,getNtoLast)
    return LastBlock[-choosebyte]

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("128.186.120.191", 31337))






#r.send("-e".encode())     # Encryption of the secret message
#x = r.recv(1024).decode()
#r.send("-e".encode())
#y = r.recv(1024).decode()
x = requestServer('')

Ciphertext, IV = GetInfo(x)
#CT2, IV2 = GetInfo(y)
#CTencode = bytes(Ciphertext)
#CT = bytes(CT2)
print("Ciphertext")
print(Ciphertext)
print("IV")
print(IV)
print("new line")
d = sliceBlocks(Ciphertext)
print(d)
print("sasd")

b=d[0]
d[-1]=b
a= d[-1]
c = xor(d[0], IV)
print(c)
print("assdad")
print(LastNbyte(c,1,1))

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
