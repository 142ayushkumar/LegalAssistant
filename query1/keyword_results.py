from sklearn.neighbors import KDTree
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import string
import re

COSTHRESH = 0.55
import pickle

# EMBEDDING_FILE = '../data/embeddings/glove.840B.300d/glove.840B.300d.txt'

with open("embed_dict.pkl",'rb') as f:
    embeddings_index = pickle.load(f)

with open("file_to_words_tf_idf.json") as f:
    file_keywords = json.load(f)

keywords = {}
# To create a tree
for filename in file_keywords:
    for word in file_keywords[filename]:
        if word in keywords:
            keywords[word] +=1
        else:
            keywords[word] = 1

# with open("legal_words.json") as kfile:
#     keywords = json.load(kfile)

key_index = {}
index_key = {}
keyword_matrix = []
sz = len(embeddings_index.get("court"))
idx = 0
for i, key in enumerate(reversed(sorted(keywords.items(), key=lambda x: x[1]))):
    if key[0] in embeddings_index:
        key_index[key[0]] = idx
        index_key[idx] = key[0]
        keyword_matrix.append(embeddings_index.get(key[0]))
        idx+=1
    # else:
    #     index_key[i] = key[0]
    #     keyword_matrix.append(np.array([100] * sz))
    #     print(key[0] + " not found")


keyword_matrix = np.array(keyword_matrix)
print(keyword_matrix.shape)
tree = KDTree(keyword_matrix)

def get_similar_words(inword, numwords):
    if inword not in embeddings_index:
        return []
    dist, ind = tree.query(embeddings_index.get(inword).reshape(1,-1),k=numwords)
    simlist = []
    for hkey in ind[0]:
        simlist.append(index_key[hkey])
        # print(index_key[hkey])
    return simlist

def get_keyword(lstkeys):
    actual_word = {}
    for word in lstkeys:
        similar_words = get_similar_words(word,1)
        if len(similar_words)==0:
            continue
        if cosine_similarity(embeddings_index.get(similar_words[0]).reshape(1,-1),embeddings_index.get(word.lower()).reshape(1,-1))[0] > COSTHRESH:
            actual_word[similar_words[0]] = word
    return actual_word

def get_similar_cases(lstkeys,lstcase,topn):
    keywords = get_keyword(lstkeys)

    case_score = {}
    for casename in lstcase:
        case_score[casename] = []
        if casename in file_keywords:
            for word in file_keywords[casename]:
                if word in keywords:
                    case_score[casename].append(keywords[word])

    similar_cases = []
    for i,key in enumerate(reversed(sorted(case_score.items(), key=lambda x: len(x[1])))):
        if i == topn:
            break
        similar_cases.append((key[0],key[1]))
    return similar_cases

if __name__=="__main__":
    query = "India, &tax,alter, earnings & partner"
    punctuations = string.punctuation
    pattern = r"[{}]".format(punctuations)
    lstkeys = re.split(pattern,query)
    lstkeys = [word.strip() for word in lstkeys]
    lstcase = ["1953_A_1"]
    print(get_similar_cases(lstkeys,lstcase,10))



#todo : put similar words together