import sys

def main():
    word = sys.argv[1]
    list=anagram(word)
    outfile=open('anagram_out.txt','w')
    for i in sorted(list):
        #print(i,file=outfile)
		outfile.write(i)
		outfile.write("\n")
        #print(i)
        

def anagram(word):
    if len(word) <=1:
        yield word
    else:
        #get anagrams word after 1st char
        for substr in anagram(word[1:]):            
            for i in range(len(word)):                
                yield substr[:i] + word[0:1] + substr[i:]


if __name__ == "__main__":main()