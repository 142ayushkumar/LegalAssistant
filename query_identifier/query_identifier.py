import numpy as np
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
# from rake_nltk import Rake
import json
import re
stop_words = set(stopwords.words('english'))


min_thresh_len = 50
################## Methods ###################
# query 1 -> minimal number of stopwords ratio
# query 2 -> ACT or abberviations match 
# query 3 -> v, vs, versus comes in middle
# query 4 -> long para, stopwords ratio more
##############################################

# def hasNumbers(string) :
#     return bool(re.search(r'\d', string))

def is_query2(query) :
    query = query.lower()

    fd = open('abbreviation_mapping.json')

    abberviations = json.load(fd)
    
    query_words = re.split(' |, |\. ', query)

    if "act" in query_words or "bill" in query_words :
        return 2

    for key in abberviations:
        if key.lower() in query_words and key.lower() not in stop_words:
            return 2

    return -1




def is_query3(query) :
    query = query.lower()

    query = query.replace('.', '')

    if query.find(" v ") != -1 or query.find(" vs ") !=-1 or query.find(" versus ") !=-1:
        return 3
    else:
        return -1


def is_query4(query) :
    query = query.lower()

    query_words = re.split(', |\. | ', query)

    if len(query_words) < 8:
        return -1
    
    stop_count = 0
    count = 0

    for word in query_words:
        if word == "":
            continue
        if word in stop_words:
            stop_count += 1
        count += 1

    if count == 0:
        return -1
        
    stop_count /= count
    
    if stop_count > 0.3:
        return 4
    else:
        return -1
        
    
def query_identifier(query) :

    # query 2
    type_of_query = is_query2(query)

    if type_of_query is 2 :
        return type_of_query

    # query 3
    type_of_query = is_query3(query)

    if type_of_query is 3:
        return type_of_query
    
    # query 4
    type_of_query = is_query4(query)

    if type_of_query is 4:
        return type_of_query

    return 1


# print ("Enter query")

# query = input()

# print(query_identifier(query))
