# `python Testing1.py`  or `python Testing1.py <int>` 
# give argument an integer if want pickle for [num*1000 : (num+1)*1000] only

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from tqdm import tqdm
import pickle 
import sys

LANGUAGE = "english"
SENTENCES_COUNT = 5
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)


def summarize_func(file_path):
    try:
        parser = PlaintextParser.from_file(file_path, Tokenizer(LANGUAGE))
        sentences = []
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            sentences.append(str(sentence))
        return " ".join(sentences)
    except Exception as e:
        print("Exception : ", e)
        return "__NULL__"


# In[21]:

list_file = []
import os
import json
from os.path import join

with open('../data/case_to_subjects.json') as f:
    data = json.load(f)

for root, dirs, files in os.walk('../data/OpenSoft-Data/All_FT/'):
    for f in files:
        fp = join(root, f)
        list_file.append(fp)
# list_file = list_file[:100]
len(list_file)

texts = []
labels = []
pickle_dir = '../data/pickled/'
if len(sys.argv)!=1:
    num = int(sys.argv[1])*1000
    list_file = list_file[num:num+1000]

for file in tqdm(list_file):
    #print(i)
    text = summarize_func(file)
    filename = file.split('/')[-1][:-4]
    label = data[filename]
    texts.append(text)
    labels.append(label)
    with open(pickle_dir+filename+'.pkl','wb') as f:
        pickle.dump([text,label],f)
# print(documents[4])
print(len(labels))
print(len(texts))
with open('../data/num.txt','w+') as f:
    f.write(sys.argv[1]+'\n')
