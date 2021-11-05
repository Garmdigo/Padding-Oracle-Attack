import socket
import socket
import base64
import math
def splitBlocks(message):
    Size = len(message)
    Slices = []
    Increment =int( math.floor(Size/16))
    for i in range(Increment):
        Slices.append(message[i*16:(i+1)*16])
    print Slices
    return Slices
def XOR(val1,val2):
    val1 = bytearray(val1)
    val2 = bytearray(val2)
    return bytearray([val1[i]^val2[i] for i in range(len(val1))])
def AddPadding(Value):
    padding = 16 - (len(string)%16)
    return Value + bytearray([padding for _ in range(padding)])
def CheckPadding(value):
    data = bytearray(value)
    expected_padding = data[-1]
    for byte in data[len(data)-expected_padding -1]:
        if byte != expected_padding:
            raise ValueError("Incorrect Padding.")
    return str(data[:len(data)-expected_padding])

def findBytes(blocks):
    CPrime = bytearray([b for b in blocks[0]])
    plaintext_byte = bytearray([0 for __ in range(16)])

    for i in range(16):
        expected_padding = bytearray([0 for __ in range(16-i)] + [(i+1) for __ in range(i)])
        CPrime = XOR(XOR(expected_padding,plaintext_byte),blocks[0]);
        for byte in range(blocks[0][15-i]+1,256) + range(0,blocks[0][15-i]+1):
            CPrime[15-i] = byte
            E = str(CPrime + blocks[1])
 
            to_test = base64.b64encode(E)
            print("Expected padding is" ,expected_padding)
            print ("E is " ,E)
            print("to_test is ",to_test)
            try:
                Combine = "-V "+ to_test
                Encode = Combine.encode()
                #print Encode
                r.send(Encode) # Valid ciphertext and IV
                x = r.recv(1024).decode()
                plaintext_byte[15 - i]  =  (byte ^ (i+1)^ blocks[0][15-i])
            except:
                pass
    return (''.join([chr(b) for b in plaintext_byte if b >16]))

def find_plaintext(Cipher):
    #HexToBinary = bytearray.fromhex(Cipher)
    Cipher = bytearray(base64.b64decode(Cipher))
   # print  "HASSDASD",HexToBinary
   # print Cipher
    blocks = splitBlocks(Cipher)
    plaintext = ""
    for i in range (len(blocks)-1):
        plaintext += findBytes(blocks[i:i+2])
    print (plaintext)

def GetCiphertext(Cipher):
    C = Cipher.split("\\n")[1].split("\\n")
    iv =   Cipher.split("IV")[1].split("'")
    CipherText = C[0].replace(" ","")
    IV = iv[1].replace("'","")
    return CipherText,IV
def HexToBinary(val):
    val = "{0:08b}".format(int(val, 16)) 
    return val
def BinaryToHex(Val):
    hexadecimal_string = hex(Val)
    return hexadecimal_string

if __name__ == "__main__":
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect(("128.186.120.190", 31337))
    try:
        while True:
            Plaintext = raw_input()
            r.send(Plaintext.encode())
            Encryption = r.recv(1024).decode()
            CipherText, IV = GetCiphertext(Encryption)
            print "Ciphertext :" ,CipherText
            print "IV: ",IV
            print (Output)

    except KeyboardInterrupt:
        r.close()
   # r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # r.connect(("128.186.120.190", 31337))
   # r.send("-e".encode())     # Encryption of the secret message
   # EM = r.recv(1024).decode()
   # Ciphertext,IV = GetCiphertext(EM)
   # Ciphertext = bytearray.fromhex(Ciphertext)
    
   # #print (EM)
   # Command =  "abcdef0123456789"
   # Encode =("-e "+ Command).encode()
   # #print("Command is ",Command)
   # #print("Encode is ",Encode)
   # r.send(Encode) # Encryption of abcdef0123456789 || message
   # EMM = r.recv(1024).decode() # EMM = Encryption M || MM
   # print "EMM is ",EMM
   # Ciphertext,IV = GetCiphertext(EMM)
   # Ciphertext = bytearray.fromhex(Ciphertext)

   # print(Ciphertext)
   # find_plaintext(Ciphertext)

   # #print ("Decode is ",EMM)

   # Command1 = "6a9215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810 659a4a7cf4273befce277e5336202d69"
   # Encode1 =("-V "+ Command1).encode()
   # r.send(Encode1) # Valid ciphertext and IV
   # x = r.recv(1024).decode()
   ## find_plaintext(x)
   # print x


   # Command2 ="6a9215b64a244b92b84dbe7cc58a5d02e8f029f432f8e931c8add86808118c5c8af29756f6d6ff85ae16ad77dc0b8221816c1dda9825f9a407b03d3f9a817160715f0b89abf9f1213bf45f464730b810 659a4a7cf4273befce277e5336202d6a"
   # Encode2 =( "-V "+ Command2).encode()
   # r.send(("-V "+ Command2).encode()) # Invalid (flipped IV bit)
   # x = r.recv(1024).decode()
   # print x




r.close()
