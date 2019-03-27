import pickle
import keras
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import json
import operator

from sklearn.metrics.pairwise import cosine_similarity
import starwrap as sw
import os
import json


tokenizer = None
thres_all = None
one_hot = None
model = None
json_data = None
category_data = None
def load_init():
    print("1")
    global tokenizer, thres_all, one_hot, model, json_data, category_data
    with open('query4/data/model/tokenizer.pkl','rb') as f:
        tokenizer = pickle.load(f)
    with open('query4/data/model/thresholds.pkl','rb') as f:
        thres_all= pickle.load(f)
    with open('query4/data/model/labeler.pkl','rb') as f:
        one_hot = pickle.load(f)
    
    model = keras.models.load_model('query4/data/model/weights.18.hdf5')
    
    with open('query4/data/citation/case_ranking/subject_to_case.txt', 'r') as file:
        json_data = file.read()
        category_data = json.loads(json_data)
        
    
def ranker(query):
    global thres_all, tokenizer, one_hot, model
    sequences_train = tokenizer.texts_to_sequences(query)
    sequences_matrix = pad_sequences(sequences_train, maxlen=100, padding='pre', truncating='pre')
    pred = model.predict(sequences_matrix,batch_size=1,verbose=1)
    thres_all = np.array(thres_all)
    z = np.array(pred)
    z = np.squeeze(z,axis=2)
    z = z.transpose()
    z = np.greater(z,thres_all)
    z = z.astype(int)
    z = one_hot.inverse_transform(z)
    return z

def give_best_cases(label_names):
    '''
        In this function, give the input as a list of labels
        Note - the name of labels must match exactly with that in subject_to_case.txt
    '''
    global json_data, category_data
    case_score = dict()
    label_count = dict()
    for labels in label_names:
        # print(labels)
        for cases in category_data[labels]:
            case_score[cases] = 0
            if cases not in label_count:
                label_count[cases] = 1;
            else:
                label_count[cases] = label_count[cases] + 1;

    for labels in label_names:
        with open("query4/data/citation/case_ranking/"+labels + '.txt', 'r') as file:
            json_data = file.read()
            label_data = json.loads(json_data)
        for case in label_data:
            case_score[case] = case_score[case] + label_data[case]*len(label_data) 

    case_score = sorted(case_score.items(), key = operator.itemgetter(1))
    case_score.sort(key = lambda z: label_count[z[0]])
    case_score.reverse()
    return case_score[:100]


def case_ranker(q,file_lists):
    arg = sw.args()
    arg.trainFile = './input.txt'
    arg.testFile = './input.txt'
    arg.trainMode = 5
    test_dir = 'query4/data/ranker/All_FT/'

    sp = sw.starSpace(arg)
    sp.init()

    MIN_SENTENCE_LEN = 10

    def get_sentences(fp):
        doc = fp.read()
        all_sentences = doc.split('.')
        sentences = []
        for s in all_sentences:
            if(len(s)>=MIN_SENTENCE_LEN):
                sentences.append(s)
        return sentences

    query = q
    qvec = np.array(sp.getDocVector(query, ' '))
    doc_score = {}

    for file in file_lists:
        fp = open('query4/data/ranker/All_FT/'+file)
        sentences = get_sentences(fp)

        if(len(sentences)==0):
            doc_score[file] = 0
            continue
    #   print("here")
        sc = 0
        for s in sentences:
            vec = np.array(sp.getDocVector(s, ' '))
            curr_sc = cosine_similarity(qvec,vec)
            sc += curr_sc[0][0]

        sc = sc/len(sentences)
        # print("sc = ", sc)
        doc_score[file] = sc
    return doc_score


def find_cases(q):
    cat_list = ranker([q])[0]
    x = give_best_cases(cat_list)
    sum_list = []
    file_lists = []
    for file_tuple in x:
        file = file_tuple[0]+".txt"
        sum_list.append(open("query4/data/ranker/All_FT/" + file).read())
        file_lists.append(file)
    with open('./input.txt','w') as f:
        f.write(" ".join(sum_list))

    doc_score = case_ranker(q, file_lists)
    final_file_list = []
    for key, value in sorted(doc_score.items(), key=lambda x: x[1],reverse=True):
        final_file_list.append(key)
    return final_file_list





#one time function calls

# load_init()

import time
start_time = time.time()

if __name__ == "__main__":
    q = '''How to sue my lawyer'''
    x = find_cases(q)
    print(x)
    print("Time: ", time.time()-start_time)