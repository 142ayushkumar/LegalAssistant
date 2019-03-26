import numpy as np 
from rake_nltk import Rake
import json
import re

min_thresh_len = 50
################## Methods ###################
# query 1 -> minimal number of stopwords ratio
# query 2 -> ACT or abberviations match 
# query 3 -> v, vs, versus comes in middle
# query 4 -> long para, stopwords ratio more
##############################################

def hasNumbers(string) :
    return bool(re.search(r'\d', string))

def is_query3(query) :
    query = query.lower()
    if query.find(" v ") or query.find(" vs ") or query.find(" v.s. ") or query.find(" v.s ") or query.find("versus") :
        return 100
    else :
        return -1

def is_query2(query) :
    query = query.lower()
    if query.find("act") or query.find("bill") :
        return 100
    else if :
        
        return -1

def is_query4(query) :
    query = query.lower()
    length = query.length() 
    with open('stopwords.json') as fp :
        stopwords_list = json.load(fp)
    if length > min_thresh_len :
        return 4
    else :
        
    

def identify_query_type(query) :

    # query 3
    type_of_query = is_query3(query)

    if type_of_query is 3 :
        return type_of_query

    # query 2
    type_of_query = is_query2(query)

    if type_of_query is 2 :
        return type_of_query
    
    # query 4
    type_of_query = is_query4()


print ("Enter query")

query = raw_input ()


# r = Rake(stopwords=stopwords_list)
# r.extract_keywords_from_text(query)

# D = dict(r.get_word_frequency_distribution())
# print D

identify_query_type(query)
