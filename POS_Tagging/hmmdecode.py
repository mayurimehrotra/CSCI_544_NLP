import sys
import pickle
from collections import Counter,defaultdict

backpointer = defaultdict(Counter)
probDict = defaultdict(Counter)

def usage():
    print "python hmmdecode.py /path/to/input"

def decode():
    model_file = open("hmmmodel.txt", "rb")
    out_file=open("hmmoutput.txt","wb")
    #test_file_path = open("test.txt", "r")
    test_file_path=open(sys.argv[1],"r")

    dictionary = pickle.load(model_file)
    states = dictionary['transmission']['nextStates']

    for line in test_file_path:

        words= line.strip().split()
        lastIndex = len(words)

        possibleStateList=getPossStateList(words[0],dictionary,states)
        if len(possibleStateList) == len(states)-1:
            for state in states:
                if state != "q0:":
                    probDict[state][0] = dictionary["transmission"]["q0"][state]
                    backpointer[state][0] = "q0"
        else:
            for state in possibleStateList:
                probDict[state][0] = dictionary["transmission"]["q0"][state] * dictionary["emission"][state][words[0]]
                backpointer[state][0] = "q0"
        #print "1",backpointer

        for i in range(1, lastIndex, 1):
            possibleStateListCurr = getPossStateList(words[i], dictionary, states)
            possibleStateListPrev  = getPossStateList(words[i-1], dictionary, states)
            #print words[i], "current" , possibleStateListCurr ,"prev" ,possibleStateListPrev

            if len(possibleStateListCurr)==len(states)-1 :  #unknown word
                for state1 in possibleStateListCurr:
                    maxProb = -1000
                    for state2 in possibleStateListPrev:
                        temp = dictionary["transmission"][state2][state1] * probDict[state2][i - 1]
                        if temp > maxProb:
                            maxProb = temp
                            probDict[state1][i] = temp
                            backpointer[state1][i] = state2
            else:
                for state1 in possibleStateListCurr:
                    maxProb=-1000
                    for state2 in possibleStateListPrev:
                        temp= dictionary["transmission"][state2][state1] * dictionary["emission"][state1][words[i]] * probDict[state2][i-1]
                        if temp>maxProb:
                            maxProb=temp
                            probDict[state1][i]=temp
                            backpointer[state1][i]=state2

        maxValue=-1000
        lastState=""
        lastWordTagList=getPossStateList(words[lastIndex-1],dictionary,states)
        for state in lastWordTagList:
            if probDict[state][lastIndex-1]>maxValue:
                maxValue=probDict[state][lastIndex-1]
                lastState=state

        # print "lastState", lastState
        # print "2 backpointer",backpointer
        # print "probDict", probDict

        outputString = words[lastIndex - 1] + "/" + str(lastState)

        for x in range(lastIndex - 1, 0, -1):
            tag = str(backpointer[lastState][x])
            outputWord = words[x - 1]
            lastState= backpointer[lastState][x]
            outputString = outputWord + "/" + tag + " " + outputString

        #print outputString
        out_file.write(outputString)
        out_file.write("\n")

        probDict.clear()
        backpointer.clear()
        line = ""

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(0)
    else:
        decode()


def getPossStateList(word,dictionary,states):
    possibleStateList=[]
    for state in states:
        if dictionary["emission"][state][word] != 0:
            possibleStateList.append(state)
    if len(possibleStateList)==0:
        for state in states:
            if state != "q0":
                possibleStateList.append(state)

    return possibleStateList


if __name__ == "__main__" :main()