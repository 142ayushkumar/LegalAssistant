# Extracts keywords from case documents and lemmatizes them and stores them in 
# a dictionary of format file->word->frequency
# Install rake_nltk using 'pip install rake-nltk' 
# Github repo-https://github.com/csurfer/rake-nltk
# Install the following components of nltk- corpus,stem,wordnet
# A stopwords.json file contains stopwords
# Input -Case documents, Stopwords list
# Output-Dict file->word->frequency
# Function- 
# 1. Rake tokenizes and filters words according to the stopwords list and returns all 
# the words in a file with their frequency. 
# 2. nltk pos_tagger is used to identify word tag and alongwith nltk lemmatizer, gives lemmatized
# keyword.


from rake_nltk import Rake
import json
import os
import collections
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet

file_path = '../../DATA/All_FT/'
stopwords_file_path='./'

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def is_alpha(s):
  for c in s:
    if c < 'a' or c > 'z':
      return False
  return True

def get_filelist():
  file_list=[]
  for path, subdirs, files in os.walk(file_path):
      for filename in files:
        file_list.append(str(os.path.join(filename)))
      file_list = sorted(file_list)
  return file_list

def extract_lemmatize_dictionary(file_list):
  with open(stopwords_file_path+'stopwords.json') as fp:
    stopwords = json.load(fp)

  r = Rake(stopwords=stopwords)

  file_to_words = {}

  lemmatizer = WordNetLemmatizer() 

  file_list = sorted(file_list)

  i = 0

  for f in file_list :

    counter = collections.Counter()

    i = i + 1
    print "Processed ", (i*100.0) / len(file_list), "%"

    lines = [line.rstrip('\n') for line in open(file_path + f)]
    for line in lines[6 : -2] :

      r.extract_keywords_from_text(line)
      d = dict(r.get_word_frequency_distribution())
      lemmatized={}
      
    
      for k, v in d.items():
        if not is_alpha(k) or len(k) < 3:
          d.pop(k)

      for k,v in d.items():
        w = []
        w.append(k)
        tag = get_wordnet_pos(nltk.pos_tag(w)[0][1])
        if tag != '':
          lem=lemmatizer.lemmatize(k,tag)
          if len(lem) < 3 :
            continue
          if lem in lemmatized :
            lemmatized[lem] = lemmatized[lem] + v
          else:
            lemmatized[lem] = v

      counter.update(lemmatized)

    file_to_words[f]=dict(counter)
    


  with open('file_to_words.json', 'w') as fp:
      json.dump(file_to_words, fp, sort_keys=True, indent=3)

if __name__ == '__main__':

  file_list = get_filelist()

  extract_lemmatize_dictionary(file_list)