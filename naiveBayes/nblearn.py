"""
Author: Mayuri Mehrotra
Task: Applied NLP CSCI 544 HW2. Naive Bayes Learn model. 
Date: 01/29/2015

usage: python3 nblearn.py PATH/TO/INPUT
"""

import sys
import glob
import pickle
import os
from collections import defaultdict,Counter


dictionary = defaultdict(Counter)
total_vocab = Counter()
stop_words={'a', 'about', 'above', 'after', 'again','against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'}

"""help to user to run program"""
def usage():
	print ("usage: python3 nblearn.py PATH/TO/INPUT")

def add_to_dict(line,path):

	"""define the 4 categories"""
	category = ''
	if "negative" in path and "deceptive" in path:
		category = 'negative_deceptive'
	elif "negative" in path and "truthful" in path:
		category = 'negative_truthful'
	elif "positive" in path and "deceptive" in path:
		category = 'positive_deceptive'
	elif "positive" in path and "truthful" in path:
		category = 'positive_truthful'
	
	dictionary['classes'][category] += 1

	"""tokenize the line into words and add each word with updated count to dictionary"""	
	for word in line.strip().split():
		if word.lower() not in stop_words:
			dictionary[category][word.lower()] += 1 
			total_vocab[word.lower()] += 1

def main():

	"""check input args and open files"""
	if len(sys.argv) !=2 :
		usage()
		sys.exit(0)
	else:
		train_data_path= sys.argv[1]
		model_file= open("nbmodel.txt","wb")

		"""traversing the root directory  --->  negative_polarity, positive_polarity"""
		sub_directories=glob.glob(train_data_path+"/*_polarity")
		#print sub_directories
		
		"""traversing polaity directory into sub directories ---> truthful & deceptive"""
		for item in sub_directories:
			sub_folders=glob.glob(item+'/*')
			#print sub_folders

			"""traversing further deep into folders"""
			for sub_item in sub_folders:
				folds=glob.glob(sub_item+'/*')				
				for fold_file in folds:					
				 	files=glob.glob(fold_file+'/*')				 					 
				 	for file_name in files:
				 		file_handler =open(file_name,'r')
				 		
				 		"""read each line and add to the dictionary with file name"""
				 		for line in file_handler:				 			
				 			add_to_dict(line,file_name)

				 		file_handler.close()

	dictionary['TRAIN_DATA']['total_vocab'] = len(total_vocab.keys())
	#print dictionary	

	"""Write the dictionary to the model file (argv[2]) using the pickle module"""
	"""The pickle module implements binary protocols for serializing and de-serializing a Python object structure"""
	pickle.dump(dictionary,model_file, protocol=pickle.HIGHEST_PROTOCOL)
	
	"""close the opened files"""
	model_file.close()

"""call the main function"""
if __name__ == "__main__" : main()