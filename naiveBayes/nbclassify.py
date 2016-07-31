import sys
import glob
import pickle
import math
import os
from collections import defaultdict,Counter

stop_words={'a', 'about', 'above', 'after', 'again','against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'}

"""help to user to run program"""
def usage():
	print ("usage: python3 nblearn.py PATH/TO/INPUT")

def bayesian_classifier(line,dictionary):
	totalClasses = len(dictionary['classes'].keys())
	max_class = (-1E6,'')
	for label in dictionary['classes'].keys():
		total_classes_count = float(sum(dictionary['classes'].values()))
		priors = math.log(dictionary['classes'][label] / total_classes_count)
		#print(priors)
		n = float(sum(dictionary[label].values()))
		#print(n)
		
		total_vocab = dictionary['TRAIN_DATA']['total_vocab']
		#print('total_vocab: ' + str(total_vocab))
		
		words = line.split()
		for word in words: 
			if word.lower() not in stop_words:
				priors = priors + math.log(max(  ( (dictionary[label][word]+1) / (n+total_vocab) ), dictionary[label][word]/n ))
				#print(priors)
			
		if priors > max_class[0]:
			max_class = (priors,label)

	return max_class[1]


def main():
	if len(sys.argv) !=2 :
		usage()
		sys.exit(0)
	else:
		train_data_path= sys.argv[1]
		model_file=open('nbmodel.txt','rb')
		out_file=open('nboutput.txt','w')
		dictionary=pickle.load(model_file)
		rootDir = sys.argv[1]
		for dirName, subdirList, fileList in os.walk(rootDir):			
			#if "fold1" in dirName:
			for file_name in fileList:
				if "LICENSE" not in file_name and "README" not in file_name:
					filepath = os.path.join(dirName, file_name)
					file_handler = open(filepath,'r')
					#print file_name
					
					for line in file_handler:
						predicted_label = bayesian_classifier(line,dictionary)

						label=''
						if "negative" in predicted_label and "deceptive" in predicted_label:
							label='deceptive '+'negative '+file_name									
						elif "negative" in predicted_label and "truthful" in predicted_label:
							label='truthful '+'negative '+file_name									
						elif "positive" in predicted_label and "deceptive" in predicted_label:
							label='deceptive '+'positive '+file_name									
						elif "positive" in predicted_label and "truthful" in predicted_label:
							label='truthful '+'positive '+file_name			
						
						print label
						out_file.write(label)
						out_file.write("\n")
									
					file_handler.close()

	model_file.close()
	out_file.close()

if __name__ == '__main__':main()