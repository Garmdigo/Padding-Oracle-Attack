#!/usr/bin/python3           # This is client.py file

import socket
import math
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Port = 31337
Port2 = 31336
s.connect(("128.186.120.190", Port2))

def XOR(A,B):
    return hex(int(A, 16) ^ int(B, 16))[2:]

def getMessage():
    Input = " "
    Encode = ("-e "+ Input).encode()
    s.send(Encode)
    Output = s.recv(1024).decode()
    CipherText, IV,CipherTextSize = GetServerInfo(Output)
    counter = 2
    Input2 = 'FF'
    Run = True
    Padding = 0
    while Run:   
        Encode = ("-e "+ Input2).encode()
        s.send(Encode)
        Output = s.recv(1024).decode()
        CipherText2, IV2,CipherTextSize2 = GetServerInfo(Output)
        if CipherTextSize != CipherTextSize2:
            Run = False
        else:
            counter += 2 
            Input2 +='FF'
    counter /=2
    counter = int(counter)
    if counter == 16:
        counter = 15
    Padding = counter
   # print("Padding is", Padding)
    plaintext = ""
    NewIV = ""
    blocks = splitBlocks(CipherText2)
    blockSize = len(blocks)
    BlockContent =""
    CT =""
    IV =""
    Length = ""
    for i in range (blockSize-1):
        for x in range(32):
            if x % 2 == 0:
                Input = Padding * 'aa' 
                Encode = ("-e "+ Input).encode()
                s.send(Encode)
                Output = s.recv(1024).decode() 
                if i == 0:
                    IV = GetIVInfo(Output)
                    CT = GetCipherTextInfo(Output)
                    BlockContent = splitBlocks(CT)
                    Length = GetLengthInfo(Output)
                   # print("Bloooockkkk",listtstring(BlockContent))
                    #FirstTwoBytes, Output = stripCipherText(FirstRoundCT)
                else:
                    Length = GetLengthInfo(Output)
                    IV = BlockContent[i-1]
                    CT = GetCipherTextInfo(Output)
                run = True
                while run:
                    Store = []
                    temp = ''
                    tracker = 0
                    Size2 = len(CT)
                    #print("CT: is",CT)
                   # print("Block is",SizeOfBlocks)
                    for r in range(Size2):
                        temp +=CT[r]
                        tracker +=1
                        if tracker ==32:                         
                            Store.append(temp)
                            tracker = 0
                            temp = ''
                           # print("Store is", Store)
                    
                   # print("Store sass ",Store)         
                    Size = len(Store)
                   # print("Original",Store)

                    Store.remove(Store[Size-1])
                    
                   # print("Remove",Store)
                   # print("Block is ",BlockContent[i+1])

                    Store.insert(Size,BlockContent[i+1])
                   # print("Insert",Store)

                    temp = ''
                    for L in Store:
                        temp += L

                    #print ("Temp is",temp)                  
                    Combine = "-v "+ temp +" "+ IV
                    Encode = Combine.encode()
                    s.send(Encode) 
                    Output = s.recv(1024).decode()
                    #print(Output)
                    
                    #print("Before If statement, IV",IV)
                    #print("Before If statement, Store",Store)
                    #print("Before If statement, Padding",Padding)
                    if Output =="Valid":
                        run = False
                plaintext += XorTChar(Store,str(Padding),IV)
    print("The Message is ",plaintext)

def XorTChar(Block,padding,IV):
    IVB = stripIV(IV)
   # print("In function, IV",IVB)

    Padding = padding
   # print(" In function, padding",padding)

    BlockStringVersion = listtstring(Block)
    IVBXORPADDING = XOR(IVB,Padding)
   # print("In function, Xoring IV and Padding",IVBXORPADDING)
    B = stripCT(BlockStringVersion)
   # print("BlockSlice",B)
    Results = XOR(B,IVBXORPADDING)
    #print("results",Results)
    #print(type(Results))
    ascii_string = ''.join(chr(int(Results[i:i+2], 16)) for i in range(0, len(Results), 2))
   # print(ascii_string)
    #ascii_string = chr(int("0x"+Results,16))
    ##ascii_string = binascii.unhexlify(Results)
    #print("ascii version", ascii_string)
    return ascii_string


def stripIV(IV):
    LastByte = IV[-2:]
    return LastByte

def stripCT(Cipher):
    SecondtoLastB = Cipher[-4:-2]
    return SecondtoLastB
    


              
    #print (plaintext)
def listtstring(s):
    str1 = ""      
    for ele in s:  
        str1 += ele       
    return str1  
def GetServerInfo(Output):
    TotalByteLength = Output.split(" ")[1].split("\\")
    C = Output.split("\\n")[1].split("\\n")
    iv =   Output.split("IV")[1].split("'")
    CipherText = C[0].replace(" ","")
    IV = iv[1].replace("'","")
    return CipherText,IV,TotalByteLength[0]
def GetCipherTextInfo(Output):
    TotalByteLength = Output.split(" ")[1].split("\\")
    C = Output.split("\\n")[1].split("\\n")
    CipherText = C[0].replace(" ","")
    return CipherText
def GetIVInfo(Output):
    TotalByteLength = Output.split(" ")[1].split("\\")
    C = Output.split("\\n")[1].split("\\n")
    iv =   Output.split("IV")[1].split("'")
    CipherText = C[0].replace(" ","")
    IV = iv[1].replace("'","")
    return IV
def GetLengthInfo(Output):
    TotalByteLength = Output.split(" ")[1].split("\\")
    return TotalByteLength[0]
def splitBlocks(message):
    Size = len(message)
    Slices = []
    Increment =int( math.floor(Size/16))
    for i in range(Increment):
        Slices.append(message[i*16:(i+2)*16])
    return Slices

try:
    getMessage()
        #data = input()
        #s.send(data.encode())
        #Output = s.recv(1024).decode()
        #CipherText, IV,Length = GetServerInfo(Output,data)
        #print (Output)

except KeyboardInterrupt:
    s.close()
