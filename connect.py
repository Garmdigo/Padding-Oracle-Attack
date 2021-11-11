import socket
from binascii import unhexlify, hexlify
from itertools import cycle
import base64

def GetInfo(Cipher):
    C = Cipher.split("\\n")[1].split("\\n")
    iv =   Cipher.split("IV")[1].split("'")
    CipherText = C[0].replace(" ","")
    IV = iv[1].replace("'","")
    return CipherText,IV

def xor(arg1,arg2):
    return hexlify(''.join(chr(ord(arg1) ^ ord(arg2)) for arg1, arg2 in zip(unhexlify(arg1), cycle(unhexlify(arg2)))))





r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("128.186.120.191", 31337))






r.send("-e".encode())     # Encryption of the secret message
x = r.recv(1024).decode()
r.send("00000000-e".encode())     # Encryption of the secret message

Ciphertext, IV = GetInfo(x)
print(Ciphertext)
print(IV)
CTencode = bytearray(Ciphertext, 'utf-8')
IVencode = bytearray(IV, 'utf-8')
print(x)
print(CTencode)
print(IV)
print(len(CTencode)/2)
print("Xor")
print(xor(Ciphertext,Ciphertext))
print(type(x))
print(type(CTencode))
print(type(IVencode))


#r.send("-e abcdef0123456789".encode()) # Encryption of abcdef0123456789 || message
#x = r.recv(1024).decode()
#print x.replace(" ", "")


#r.send("-V 6a9215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810 659a4a7cf4273befce277e5336202d69".encode()) # Valid ciphertext and IV
#x = r.recv(1024).decode()
#print x



#r.send("-V 6a9215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810 659a4a7cf4273befce277e5336202d6a".encode()) # Invalid (flipped IV bit)
#x = r.recv(1024).decode()
#print x




r.close()
