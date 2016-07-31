import binascii
import sys

def main():
    
    infile=open(sys.argv[1],'rb')    
    outfile=open('utf8encoder_out.txt','wb')
    inputBytesHex=infile.read(2)       #read 2 bytes at a time    
    
    while len(inputBytesHex):    	
    	hexadecimal = binascii.hexlify(inputBytesHex)
    	decimal = int(hexadecimal, 16)			# to check hex range , convert to int and check
    	binary = bin(decimal)[2:].zfill(16)
    	s = str(binary)
    	
    	if  0 <= decimal <= 127: 
    		resultString="0" + s[-7:]   		    		
    		outfile.write(chr(int(resultString[0:8],2)))    		
    		
    	if  128 <= decimal <= 2047:
    		rightStr = "10" + s[-6:]
    		leftStr ="110" + s[5:10]    		    		
    		resultString=leftStr+rightStr    		

    		outfile.write(chr(int(resultString[0:8],2)))
    		outfile.write(chr(int(resultString[8:16],2)))
    		
    	if  2048 <= decimal <= 65535:
    		rightStr="10" + s[-6:]
    		leftStr = "1110" + s[0:4]    		
    		midStr= "10" + s[4:10]
    		resultString=leftStr+midStr+rightStr    		
    		
    		outfile.write(chr(int(resultString[0:8],2)))
    		outfile.write(chr(int(resultString[8:16],2)))
    		outfile.write(chr(int(resultString[16:],2)))			

    	inputBytesHex=infile.read(2)        

if __name__ == "__main__" :main()