
import binascii

#Reading Binary file
filePath='japanese_in.txt'
fin=open(filePath,'rb')
twoBytes=list()
fin.seek(0)
byte1=fin.read(1)
byte2=fin.read(1)

while byte1!='':
    temp=bytearray([byte1, byte2])
    twoBytes.append(int('0x'+binascii.hexlify(temp),16))
    byte1=fin.read(1)
    byte2=fin.read(1)

fout=open('utf8encoder_out.txt','wb')

for i in range(0,len(twoBytes)):
    b=twoBytes[i]
    binRep=bin(b)[2:]
    #Case 1 - UTF-8 in 1 byte
    if(b>=0 and b<=127):
        if(len(binRep)>8):
            continue;
        printValue='0'*(8-len(binRep))+binRep
        fout.write(chr(int('0b'+printValue,2)))
    
    #Case 2 - UTF-8 in 2 bytes
    elif(b>=128 and b<=2047):
        if(len(binRep)>11):
            continue;           
        if(len(binRep)<11):
            binRep='0'*(11-len(binRep))+binRep
        printValue='110'+binRep[:5]+'10'+binRep[5:]
        fout.write(chr(int('0b'+printValue[:8],2)))
        fout.write(chr(int('0b'+printValue[8:],2)))
    
    #Case 3 - UTF-8 in 3 bytes
    elif(b>=2048 and b<=65535):
        if(len(binRep)>16):
            continue;
        if(len(binRep)<16):
            binRep='0'*(16-len(binRep))+binRep
        printValue='1110'+binRep[:4]+'10'+binRep[4:10]+'10'+binRep[10:]
        fout.write(chr(int('0b'+printValue[:8],2)))
        fout.write(chr(int('0b'+printValue[8:16],2)))
        fout.write(chr(int('0b'+printValue[16:],2)))