import sys
import pickle
from collections import Counter,defaultdict

dictionary_obs=defaultdict(Counter)
dictionary_trans=defaultdict(Counter)
output_dictionary=defaultdict(Counter)

def usage():
    print ("usage: python nblearn.py PATH/TO/INPUT")

def fileread():
    file_handler=open(sys.argv[1],"r")
    #file_handler = open("hello.txt", "r")
    model_file = open("hmmmodel.txt", "wb")
    for line in file_handler:
        tokens= line.strip().split()
        for i in range(0,len(tokens)-1):

            #tag=tokens[i].split("/")[1]
            #word=tokens[i].lower().split("/")[0]

            tag=tokens[i][-2:]
            word=tokens[i][:-3]

            dictionary_obs['states'][tag] +=1
            dictionary_obs[tag][word] +=1

            dictionary_trans['nextStates'][tag] +=1
            #dictionary_trans[tag][tokens[i + 1].split("/")[1]] += 1
            dictionary_trans[tag][tokens[i+1][-2:]] += 1

        dictionary_trans['nextStates']['q0'] += 1
        dictionary_trans['q0'][tokens[0][-2:]] += 1
        #dictionary_trans['q0'][tokens[0].split("/")[1]] += 1

        #dictionary_obs['states'][tokens[i+1].split("/")[1]] += 1
        #dictionary_obs[tokens[i+1].split("/")[1]][tokens[i+1].split("/")[0]] += 1
        dictionary_obs['states'][tokens[i + 1][-2:]] += 1
        dictionary_obs[tokens[i + 1][-2:]][tokens[i + 1][:-3]] += 1

    for i in dictionary_obs['states']:
        for k in dictionary_obs[i]:
            dictionary_obs[i][k] = dictionary_obs[i][k]/float(dictionary_obs['states'][i])

    # for i in dictionary_trans['nextStates']:
    #     for k in dictionary_trans[i]:
    #         dictionary_trans[i][k] = dictionary_trans[i][k] / float(dictionary_trans['nextStates'][i])

    #output_dictionary['transmission']=dictionary_trans
    output_dictionary['emission']=dictionary_obs

    #print output_dictionary

    #print dictionary_obs
    #print dictionary_trans

    count =len(dictionary_trans["nextStates"]) - 1

    for state1 in dictionary_trans['nextStates']:
        for state2 in dictionary_trans['nextStates']:
            if state2 != "q0":
                #dictionary_trans[state1][state2] +=1
                dictionary_trans[state1][state2] = (dictionary_trans[state1][state2] + 1)/ float(dictionary_trans['nextStates'][state1] + count)

    #print dictionary_trans

    output_dictionary['transmission']=dictionary_trans

    pickle.dump(output_dictionary,model_file,protocol=pickle.HIGHEST_PROTOCOL)

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(0)
    else:
        model_file=open("hmmmodel.txt","wb")
        fileread()

if __name__ == "__main__" :main()
