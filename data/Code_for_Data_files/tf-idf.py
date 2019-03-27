import json
import os
from collections import defaultdict
import math
import operator

def defaultValue():
	return 0

file_path='./File2Words/'
out='./tf-idf/'
thresh=20 # Max no. of words in a file
file_thresh= 1000 #each word should have at least this much frequency
N=(53211) # total no. of files
'''
tf-idf= freq *log(N/n) 
'''
words_n=defaultdict(defaultValue)

def get_filelist():
  file_list=[]
  for path, subdirs, files in os.walk(file_path):
      for filename in files:
        file_list.append(str(os.path.join(filename)))
      file_list = sorted(file_list)
  return file_list

def get_n():
	i=0
	for f in file_list:
		i = i + 1
   		print "Processed ", (i*100.0) / len(file_list), "%"
		with open(file_path+f) as fp:
			d = json.load(fp)

		for word in d.keys():
			words_n[word]=words_n[word]+1

def tfidf():
	i=0
	for f in file_list:
		i=i+1
		print "processed ", (i*100.0)/len(file_list),"%"
		with open(file_path+f) as fp:
			d = json.load(fp)
		
		write={}
		for word,freq in d.items():
			if words_n[word] > file_thresh:
				write[word]=freq * math.log(N/float(words_n[word]),10)

		values = sorted(write.items(), key = operator.itemgetter(1), reverse = True)

		# final=[] 
		# i=0
		# for word,score in sorted(write.items(), key = lambda kv:(kv[1], kv[0]) , reverse=True):
		# 	i=i+1
		# 	final.append(word)
		# 	if i>thresh:
		# 		break
		values = values[0:thresh]
		with open(out+f, 'w') as fp:
			for x in values:
				fp.write(str(x[0]) + '\n')
			



if __name__ == '__main__':

	file_list=get_filelist()
	get_n()
	tfidf()


