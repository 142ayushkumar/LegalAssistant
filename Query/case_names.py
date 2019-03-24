'''
From the query of type 3, extracts the case files
'''
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import json
stop_words = set(stopwords.words('english'))
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
'''
Use the dictionaries 'Cases_from_caseName.json', 'States.json' and 'reduced_dictionary.json' 
in the same directory as this code file.

Function for Query 3    
 - Returns the possible cases (case id) along with the priority in form of a score (max 200)
 - Number of parties has to be tweaked

'''
def query_3(query):
    with open('States.json') as f:
        d=json.load(f)
    '''
    if query has two parties: eg. "A v B"
    '''
    if query.find(" v ")>0:    
        party_1, party_2 = query.split(" v ")
        party1 = party_1.split(' ')
        party2 = party_2.split(' ')
        search_1 = set()
        search_2 = set()
        for word in party1:
            if word not in stop_words:
                search_1.add(word[0].upper())
            if word.isupper():
                w=process.extract(word, d.keys(), limit=1, scorer=fuzz.token_set_ratio)
                for i in w:
                    w=d[i[0]]
                party_1=party_1.replace(word, w)
        for word in party2:
            if word not in stop_words:
                search_2.add(word[0].upper())
            if word.isupper():
                w=process.extract(word, d.keys(), limit=1, scorer=fuzz.token_set_ratio)
                for i in w:
                    w=d[i[0]]
                party_2=party_2.replace(word, w)
        number_of_parties = 100
        with open('Cases_from_caseName.json') as file:
            file_dict=json.load(file)
        with open('reduced_dictionary.json') as f:
            data = json.load(f)
        parties_1=[]
        parties_2=[]
        for k in search_1:
            parties_1 += process.extract(party_1, data[k], limit = number_of_parties, scorer=fuzz.token_set_ratio)
        for k in search_2:
            parties_2 += process.extract(party_2, data[k], limit = number_of_parties, scorer=fuzz.token_set_ratio)

        selected_cases = []
        for i in parties_1:
            list_cases_party_1 = file_dict[str(i[0])]
            for j in parties_2:
                list_cases_party_2 = file_dict[str(j[0])]
                intersection = [value.encode('utf-8') for value in list_cases_party_1 if value in list_cases_party_2]
                score = i[1]+j[1]
                if intersection != []:
                    selected_cases.append([intersection[0],score])

        def sortSecond(val):
            return val[1]
        selected_cases.sort(key = sortSecond, reverse=True)
        select=[]
        for i in selected_cases:
            select.append(i[0])
        final_list = [] 
        for name in select: 
            if name not in final_list: 
                final_list.append(name) 
        return final_list
    '''
    When query has single party: eg. "A"
    '''
    else:
        search_1=[]
        number_of_parties = 1
        party1 = query.split(' ')
        with open('Cases_from_caseName.json') as file:
            file_dict=json.load(file)
        with open('reduced_dictionary.json') as f:
            data = json.load(f)
        parties_1=[]

        for word in party1:
            if word not in stop_words:
                search_1.append(word[0].upper())
            if word.isupper():
                w=process.extract(word, d.keys(), limit=1, scorer=fuzz.token_set_ratio)
                for i in w:
                    w=d[i[0]]
                query=query.replace(word, w)

        for k in search_1:
            parties_1 += process.extract(query, data[k], limit = number_of_parties, scorer=fuzz.token_set_ratio)
        selected_cases = []
        for i in parties_1:
            for j in range(min(len(file_dict[str(i[0])]),20)):
                selected_cases.append((file_dict[str(i[0])][j]).encode('utf-8'))
        return selected_cases

if __name__ == '__main__':


    q = raw_input("Enter case : ")
    '''
    Query Preprocessing
    '''
    ql=""
    for char in q:
        if char!='.' and char!=',' and char!='(' and char!=')' and char!='-':
            ql+=char
    s=ql.lower()
    a=s.find(' vs ')
    b=s.find(' versus ')
    c=s.find(' v ')
    if a>0:
        ql = ql.replace(ql[a:a+4]," v ")
    if b>0:
        ql=ql.replace(ql[b:b+8]," v ")
    if c>0:
        ql=ql.replace(ql[c:c+3]," v ")
    print(query_3(ql))