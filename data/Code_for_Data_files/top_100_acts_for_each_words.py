import json
import nltk
from nltk.corpus import stopwords
import os
import re


''' This file will generate a file containing top 100 acts for 
    each keywords in every act
    change path of files accordingly
'''
with open('../acts_ranking.json') as f:
    file = f.read()
    value = json.loads(file)

stopwords = set(stopwords.words('english'))

all_words = {}

for root, dirs, files in os.walk("/mnt/d/final/opensoft19/data/Code_for_Data_files/Central_Text"):
    for file in files:
        with open(os.path.join(root, file), "r") as auto:
            for line in auto:
                x = line.split("-->")
                x[1] = re.sub(r"""
                [,.;@#?!&$]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               " ",          # and replace it with a single space
               x[1], flags=re.VERBOSE)

                line.replace(",", " ")
                line.replace(".", " ")
                words = x[1].split()
                filename = file.split(".")[0]
                for word in words:
                    if not word[-1].isalpha():
                        word = word[:-1]
                    if len(word) > 1:
                        if not word[0].isalpha():
                            continue
                        if word.isdigit() == False or word not in stopwords:
                            if word in all_words:
                                all_words[word].append(filename)
                            else:
                                all_words[word] = []

for root, dirs, files in os.walk("/mnt/d/final/opensoft19/data/Code_for_Data_files/State_Text"):
    for file in files:
        with open(os.path.join(root, file), "r") as auto:
            for line in auto:
                x = line.split("-->")
                x[1] = re.sub(r"""
                [,.;@#?!&$]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               " ",          # and replace it with a single space
               x[1], flags=re.VERBOSE)

                line.replace(",", " ")
                line.replace(".", " ")
                words = x[1].split()
                filename = file.split(".")[0]
                for word in words:
                    if not word[-1].isalpha():
                        word = word[:-1]
                    if len(word) > 1:
                        if not word[0].isalpha():
                            continue
                        if word.isdigit() == False or word not in stopwords:
                            if word in all_words:
                                all_words[word].append(filename)
                            else:
                                all_words[word] = []

remove_words = []
for word in all_words:
    if len(all_words[word]) < 500:
        remove_words.append(word)
        continue
    all_words[word] = list(set(all_words[word]))
    all_words[word].sort(key = lambda z: value[z] if z in value else 0, reverse = True)
    all_words[word] = all_words[word][:1000] # only storing top 1000 files according to acts_ranking

for word in remove_words:
    all_words.pop(word, None)
print(len(all_words))

output = open("../word_to_acts.txt", "w")
js = json.dumps(all_words)
output.write(js)
