import json
import seaborn as sns 
import numpy as np

'''
Classes categories and sub catgory identification using tf-idf
'''

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

with open('data/Generated/matrix.json') as f:
	data = json.load(f)

thresh = 5000
final_words = []
stemmed_words = {}
i = 0
for key,values in data.items():
	if i is 0: # Skip the first key
		i+=1
		continue

	s = sum(values)
	if(s <= thresh):
		continue

	stm = stemmer.stem(key)

	if stm not in stemmed_words.keys():
		stemmed_words[stm] = ([key],s)
	else:
		stemmed_words[stm] = (stemmed_words[stm][0] + [key],s + stemmed_words[stm][1])

	final_words.append(key)

tf_tdfs = {}
### Total number of terms/words in a document/class ###
words_in_class = []
for i in range(62): # 62 classes
	print(i)
	words_in_i = 0
	for key in data.keys():
		if key not in final_words:
			continue
		words_in_i+=data[key][i]
	words_in_class.append(words_in_i)

words_in_class = np.array(words_in_class)
print(words_in_class)
np.save('data/Generated/words_in_class_tfidf.npy',words_in_class)
########################################################

'''
for stm,info in stemmed_words.items():
	og_words = info[0]
	
	for og_word in og_words:
		class_frequencies = np.array(data[og_word]).reshape(-1,1) # Per category frequencies

		tfs = np.divide(class_frequencies,1.0*words_in_class.reshape(-1,1))

		number_of_documents_with_og_word_in_class
		idf = np.log(62.0/)
'''