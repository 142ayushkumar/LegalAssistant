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

    '''
    Query Preprocessing
    '''
    ql=""
    for char in query:
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

    query = ql

    with open('Case_Abbreviations_Dictionary.json') as f:
        d=json.load(f)
    '''
    if query has two parties: eg. "A v B"
    '''
    if query.find(" v ")>0:    
        party_1, party_2 = query.split(" v ",1)
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
        number_of_parties = 300
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
                score = float(i[1]+j[1])/200
                if intersection != []:
                    if [intersection[0],score] not in selected_cases:
                        selected_cases.append([intersection[0],score])

        count=len(selected_cases)
        if count<20:
            for i in parties_1:
                for j in range(len(file_dict[str(i[0])])):
                    if count==20:
                        break
                    if [(file_dict[str(i[0])][j]).encode('utf-8'),float(i[1])/200] not in selected_cases:
                        selected_cases.append([(file_dict[str(i[0])][j]).encode('utf-8'),float(i[1])/200])
                        count+=1
        else:
            selected_cases=selected_cases[:20]

        def sortSecond(val):
            return val[1]
        selected_cases.sort(key = sortSecond, reverse=True)
        #select=[]
        #for i in selected_cases:
        #    select.append(i[0])
        #final_list = [] 
        #for name in select: 
        #    if name not in final_list: 
        #        final_list.append(name) 
        d={}
        for file in selected_cases:
            d[file[0]]=file[1]
        with open('Query_3_results.json','w') as out:
            json.dump(d,out)
    
    else:
        search_1=[]
        number_of_parties = 300
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
        count=0
        for k in search_1:
            parties_1 += process.extract(query, data[k], limit = number_of_parties, scorer=fuzz.token_set_ratio)
        selected_cases = []
        for i in parties_1:
            for j in range(len(file_dict[str(i[0])])):
                if count==20:
                    break
                if [(file_dict[str(i[0])][j]).encode('utf-8'),float(i[1])/200] not in selected_cases:
                    selected_cases.append([(file_dict[str(i[0])][j]).encode('utf-8'),float(i[1])/100])
                    count+=1
        d={}
        for file in selected_cases:
            d[file[0]]=file[1]
        with open('Query_3_results.json','w') as out:
            json.dump(d,out)

if __name__ == '__main__':

    q = raw_input("Enter case : ")
    query_3(q)
    
    