import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import json
stop_words = set(stopwords.words('english'))

d={}
dat={}
with open('Cases_from_caseName.json') as file:
	data = json.load(file)
print(data.keys())
for key in data.keys():
	key = key.encode('utf-8')
	for word in key:
		if word not in stop_words and word[0].isupper():
			d.setdefault(word[0], []).append(key)
with open('reduced_dictionary.json','w') as out:
	json.dump(d, out)