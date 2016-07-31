'''
Created on Apr 25, 2016

@author: dell
'''

from __future__ import division
import math
from collections import Counter
import sys
import os

def computeBP(candidates, referencesList):  
    c = 0  
    r = 0
    
    for i in range(0,len(candidates)):
        c += len(candidates[i])
        minDiff = sys.maxint
        minR = 0
        for reference in referencesList[i]:
            if((abs(len(reference)-len(candidates[i]))<minDiff)):
                minDiff = (abs(len(reference)-len(candidates[i])))
                minR = len(reference)
        r += minR
    print "c=",c
    print "r=",r 
        
    bp = 1
    if(c<=r):              
        bp = math.exp(1-(r/c))
    
    return bp

def findNGrams(input,n) : #value n is given as input
    ngrams = []
    
    if (n==1):
        ngrams = input
    
    else:
        if(len(input)>=n):
            for i in range (0,len(input)-n+1): #for every word in input
                gram = input[i]
                for x in range(1,n): #second parameter of range is excluded
                    gram = gram+" "+input[i+x] #concatenate grams as space separated
                ngrams.append(gram)
        
    return ngrams #return array of ngrams

def computeModifiedPrecision(candidates, referencesList, n):
    # candidates is list of tokenized candidate sentences
    #referencesList is list of tokenized references for each candidate sentence
    numerator = 0.0
    denominator = 0.0
    
    for candidate,references in zip(candidates,referencesList):
        #candidate = [c.lower() for c in candidate]
        #references = [[r.lower() for r in reference] for reference in references]
        
        # Counter for candidate        
        counts = Counter(findNGrams(candidate, n)) #Counter holds counts of every unique ngram obtained in the array
        if not counts:
            numerator += 0.0
            denominator += 0.0
        else:
            max_counts = {} #dict
            for reference in references: #for each reference in references
                
                reference_counts = Counter(findNGrams(reference, n))
                for ngram in counts:
                    max_counts[ngram] = max(max_counts.get(ngram, 0.0), reference_counts[ngram]) #find max among references
                
            #Countclip = min(Count,MaxRefCount)    
            clipped_counts = dict((ngram, min(count, max_counts[ngram])) for ngram, count in counts.items())
            
            #print clipped_counts
            #print sum(clipped_counts.values())
            numerator += sum(clipped_counts.values())
            #print numerator
            denominator += sum(counts.values())    
    
    return  numerator/denominator

def computeBLEU(candidates,referencesList,weights):
    bp = computeBP(candidates, referencesList)    
     
    p = 0.0
    p_ns = []
    for i in range(1,len(weights)+1): #generate ngrams from unigram to 4grams(4 is length of weights array)        
        p = computeModifiedPrecision(candidates, referencesList, i)
        p_ns.append(p)
    
    s = 0.0
    for w, p_n in zip(weights, p_ns): 
        if p_n:            
            s += w * math.log(p_n) 
    #When you zip() together three lists containing 20 elements each, the result has twenty elements. Each element is a three-tuple.

    return bp * math.exp(s)

candidatesFile = "G:/USC/Spring2016/NLP/Assignments/HW8/candidate-3.txt" 
#candidatesFile = sys.argv[1]
#candidatesFile = "G:/USC/Spring2016/NLP/Assignments/HW8/candidate-5.txt"
referencesPath = "G:/USC/Spring2016/NLP/Assignments/HW8/reference-3.txt" 
#referencesPath = sys.argv[2]
#referencesPath = "G:/USC/Spring2016/NLP/Assignments/HW8/reference-5"

candidates = []
referencesList = []

with open(candidatesFile,'r') as f:
    for line in f:  #remove punctuations?!?
        line = line.replace("\n","")
        tokenizedLine = line.split()
        candidates.append(tokenizedLine) #tokenize sentence and add to array  
       
if os.path.isdir(referencesPath):
    #if directory scan through all files       
    for filename in os.listdir(referencesPath): 
        reference = []    
        with open(referencesPath+"/"+filename,'r') as f:
            for line in f:  #remove punctuations?!?
                line = line.replace("\n","")
                tokenizedLine = line.split()                
                reference.append(tokenizedLine) #tokenize sentence and add to array at corresponding index
            referencesList.append(reference)   
else:    
    reference = []
    with open(referencesPath,'r') as f:
        for line in f:  #remove punctuations?!?
            line = line.replace("\n","")
            tokenizedLine = line.split()
            reference.append(tokenizedLine) #tokenize sentence and add to array at corresponding index
        referencesList.append(reference)   
            
referencesList = zip(*referencesList) #transpose          

weights = [0.25, 0.25, 0.25, 0.25]
#print candidates
#print referencesList

op_file = open("bleu_out.txt", "w")
bleu = computeBLEU(candidates, referencesList, weights)
print "bleu=",bleu
op_file.write(str(bleu))