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
    size = len(message) /2
    Bytes = message
    slices = []
    x = 0
    y = 32
    v = size % 32
    if(v):
        iter = len(message)/32
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

def getNtoLast(bytes,position):
    return bytes[-positon]
def LastNbyte(bytes,getNtoLast,choosebyte):
    LastBlock = getNtoLast(bytes,getNtoLast)
    return LastBlock[-choosebyte:]

def testOracle():
     t = requestServer("")
     Ciphertext, IV = GetInfo(t)
     d = sliceBlock(Ciphertext)
     b=d[0]
     d[-1]=b
     st = listToString(d)
     z = checkValidate(str(st), str(IV))
     return st, IV, z


def oracle(p):
     t = requestServer("")
     Ciphertext, IV = GetInfo(t)
     d = sliceBlock(Ciphertext)
     b=d[p]
     d[-1]=b
     st = listToString(d)
     z = checkValidate(str(st), str(IV))
     return st, IV, z


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

def xorTest(val, val2):
    result = xor(val, val2)
    result1 = xor(result[-2:], '15')
    return result1


def pleaseWork():
	CT, IV, val = testOracle()
        x = block =result=result2 = y = ""
        if(val == "Valid"):
                block = returnithBlock(CT, -2)
                result = xor(IV, block)
                result2 = xor(result[-2:], '0F')
                x = CT
                y = IV
        else:
                while(val!="Valid"):
                        CT, IV, val = testOracle()
                        if(val == "Valid"):
                                block = returnithBlock(CT, -2)
                                result = xor(IV, block)
                                result2 = xor(result[-2:], '0F')
                                x = CT
                                y = IV
        print(x)
        print(y)
        print(result2)
        blocks = splitBlocks(x)
        blockLen = len(blocks)
        for i in range(blockLen - 2):
		CT, IV, val = testOracle()
        	
        	if(val == "Valid"):
                	block = returnithBlock(CT, -2)
                	result = xor(IV, block)
                	result2 = xor(result[-2:], '0F')
                	x = CT
                	y = IV
        	else:
                	while(val!="Valid"):
                        	CT, IV, val = testOracle()
                        	if(val == "Valid"):
                                	block = returnithBlock(CT, -2)
                                	result = xor(IV, block)
                                	result2 = xor(result[-2:], '0F')
                                	x = CT
                                	y = IV
		       
		
		

'''
def validDecrypt(prefix):
    t = requestServer('')
    cipher, iv = GetInfo(t)
    cipherBlock = sliceBlock(cipher)
    cipherLen = len(CipherBlock)
    for i in range(cipherLen - 2):
    	st, IV, z = testOracle(i,t)
    	if(z == "Valid"):
		return st, IV, z
    	else:
        	while(z!="Valid"):
		 	t = requestServer('')
    			cipher, iv = GetInfo(t)
           		st, IV, z = testOracle(i,t)
           		if(z == "Valid"):
                 		block2 = returnithBlock(st, -2)
                  		result = xor(IV, block2)
                  		result2 = xor(result[-2:], '0F')
                  		print(result2)
	          		y = requestServer(prefix)
                  		C, I = GetInfo(y)
                  		B = prefixTest(st,C)
                  		val = checkValidate(str(B), str(IV))
                  		if(val == "Valid"):
					print("WE'RE Close")
                        		block2 = returnithBlock(st, -2)
                        		result = xor(I, block2)
                        		return B, IV, val, result2
                  		else:
                    			while(val!="Valid"):
                      			y = requestServer(prefix)
                      			C, I = GetInfo(y)
                      			B = prefixTest(st,C)
                      			val = checkValidate(str(B), str(IV))
                      			if(val == "Valid"):
                        			print("WE'RE Closer")
                        			#block = returnithBlock(B,0)
                        			block2 = returnithBlock(st, -2)
                        			print(st)
                        			print(block2)
                        			print(I)
                        			result = xor(I, block2)
                        			print(xor(result[-2:], '0F'))
                        			return B, IV, val, result

'''             
	         


r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("128.186.120.191", 31337))






#r.send("-e".encode())     # Encryption of the secret message
#x = r.recv(1024).decode()
#r.send("-e".encode())
#y = r.recv(1024).decode()

pleaseWork()
		


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
