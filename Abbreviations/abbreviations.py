import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import json
stop_words = set(stopwords.words('english'))
from fuzzywuzzy import process
from fuzzywuzzy import fuzz



raw = []
data = []

def imp_words(fd):
	
	for line in fd:
		raw.append(line)
		bracket_list = re.split('\(|\)', line)
		str_list = ""
		for i in range(len(bracket_list)):
			if i%2 == 0:
				str_list += bracket_list[i]
				str_list += " "
		data.append(str_list)


	data_words = []

	for line in data:
		bracket_list = re.split(' |-|\n|Act, |, ', line)
		li = []
		for w in bracket_list:
			if w not in stop_words and w != "":
				li.append(w)
		data_words.append(li)

	return data_words


def myfun(data_words):

	dict_abb = {}
	for i in range(len(data_words)):
		if i != len(data_words)-1 and data[i] == data[i+1]:
			continue
		st = ""
		for word in data_words[i]:
			if word[0] <= '0' or word[0] >= '9':
				st += word[0]

		if dict_abb.get(st) == None:
			dict_abb[st] = [raw[i][:-1],]
		else:
			dict_abb[st].append(raw[i][:-1])

	return dict_abb


if __name__ == "__main__":

	# fd1 = open("actlist.txt", "r");

	# data_words = imp_words(fd1)

	# dict_abb = myfun(data_words, j)

	fd2 = open("abbreviation_mapping.json", "r")

	# jsonFile = json.dumps(dict_abb)
	# fd2.write(jsonFile)

	list_of_abb = []
	abb_data = json.load(fd2)

	for key in abb_data:
		list_of_abb.append(key)

	x = input()

	x = process.extract(x, list_of_abb, limit = 1)
	# print(x)
	x = x[0][0]
	# print(x)

	if abb_data.get(x) != None:
		print(abb_data[x])

	fd2.close()