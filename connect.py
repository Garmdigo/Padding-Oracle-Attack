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


def sliceBlock(message):
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
      padding = 32 - (size % 32) 
      for i in range(padding):
	 message = message + '0'
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

def L2L2string(input):
	tmp = convertToList(input)
	return listToString(tmp)

def convertToList(input):
    lists = []
    for i in input:
        if type(i) is list:
            for j in i:
                lists.append(j)
        else:
            lists.append(i)
    return lists

def testOracle(prefix=""):
     t = requestServer(prefix)
     Ciphertext, IV = GetInfo(t)
     d = sliceBlock(Ciphertext)
     b=d[0]
     d[-1]=b
     st = listToString(d)
     z = checkValidate(str(st), str(IV))
     return st, IV, z


def oracle(p, prefix=""):
     t= requestServer(prefix)
     C, I = GetInfo(t)
     d = sliceBlock(C)
     b=d[p]
     d[-1]=b
     st = listToString(d)
     z = checkValidate(str(st), str(I))
     return st, I, z

def secondOracle(p, prefix, ci, I):

	t2=requestServer(prefix)
	C2, I2=GetInfo(t2)

	ret = prefix2ndTest(ci, C2, p)

	z=checkValidate(str(ret), str(I))
	return C2, I2, z
	

def prefix2ndTest(C, Cprime, p):
    B = sliceBlock(Cprime)
    b = B[p]                    #first block of Cprime
    D = sliceBlock(C)
    D[-1] = b                   #swap c4 to b1
    st = listToString(D)
    return st


def prefixTest(C, Cprime):
    B = sliceBlock(Cprime)
    b = B[0]			#first block of Cprime
    D = sliceBlock(C)
    D[-1] = b			#swap c4 to b1
    st = listToString(D)
    return st

def returnithBlock(ciphertext, i):
   blocks = sliceBlock(ciphertext)
   b = blocks[i]
   return b

def testLength():
	padding = ""
        counter = 0
	for i in range(0, 15):
              val="Invalid"
              while(counter!=256):
              	    CT2, I2, val=testOracle(padding)
              	    if (val=='Valid'):
                         block=returnithBlock(CT2, -2)
                         bl=I2+CT2
                         o=sliceBlock(bl)
                         result=xor(o[0], block)
                         result2=xor(result[-2:], '0F')
			 return CT2, I2, val, padding, i
		    counter = counter + 1
              padding=padding+'00'
	      print(padding)
              counter = 0
	

def pleaseWork():
	CT, I, val, pad, padlen = testLength()
	#(if padlen == 0)
	s = sliceBlock(CT)
	messagelen = len(s) -2
	message=[]
	for i in range(messagelen):
		message.append([])
        x1= y1=x = block =result=result2 = y = ""
        for i in range(messagelen):
		CT,I, val = oracle(i,pad)
        	if(val == "Valid"):
                	block = returnithBlock(CT, -2)
			bl = I + CT
			o = sliceBlock(bl)
               		result = xor(o[i], block)
               		result2 = xor(result[-2:], '0F')
                	x1 = CT
                	y1 = I
			message[i].insert(0,result2.decode('hex'))
       		else:
               		while(val!="Valid"):
                       		CT, I, val = oracle(i,pad)
                       		if(val == "Valid"):
                               		block = returnithBlock(CT, -2)	
					bl = I + CT
					o = sliceBlock(bl)
                               		result = xor(o[i], block)
                               		result2 = xor(result[-2:], '0F')
                               		x1 = CT
                               		y1 = I
					message[i].insert(0,result2.decode('hex'))
					
	padding=pad
	count = 16 - padlen	
	for j in range(messagelen):
		for i in range(0, count):
			val="Invalid"
			while(val!="Valid"):
				CT2, I2, val=secondOracle(j, padding, CT, I)
				if (val=='Valid'):
					block=returnithBlock(CT, -2)
					bl=I2+CT2
					o=sliceBlock(bl)
					result=xor(o[j], block)
					result2=xor(result[-2:], '0F')
					message[j].insert(0,result2.decode('hex'))
			padding=padding+'00'
		padding=pad	
			 				
	return(L2L2string(message))
		


r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("128.186.120.191", 31336))
print(pleaseWork())

#CT, I, val, pad, z = testLength()		
#print(pad)
#print(z)

