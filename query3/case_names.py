'''
From the query of type 3, extracts the file_names
'''
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
stop_words = set(stopwords.words('english'))
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

base_dir = ""
'''
Use the following dictionaries in the same directory as this code file:
1) 'Cases_from_caseName.json'- containing map of 'case names' to list of 'case ids',
2) 'Case_Abbreviations_Dictionary.json'- containing map of related 'abbreviations' to their 'full_form' eg: "MH": "Maharashtra"
3) 'reduced_dictionary.json'- containing map of 'First character of case names' to 'case names starting with that character'

Function for Query 3
 - Input: The case name (Type 3 query) from user
 - Output: Query_3_results.json containing a dictionary of the form {"case_id" : score, ...}
 - function: 1) query_3() pre-processes the query
             2) replaces the detected abbreviations in query by their full forms using 'Case_Abbreviations_Dictionary.json'
             3) First searches in the 'reduced_dictionary.json' by the first letter of words in processed query
             4) Then extracts the list of case_id's from 'Cases_from_caseName.json'
             5) Finally writes results to 'Query_3_results.json'
Example: Input - "state of MH v sitaram popat vetal and anr."
         Output - {"2012_S_190": 0.79, "1979_V_13": 0.79, "2001_S_122": 0.835, "2004_S_198": 1.0, "2017_S_465": 0.825, "2010_S_302": 0.8, ...} 
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

    with open(base_dir + 'Case_Abbreviations_Dictionary.json') as f:
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
        with open(base_dir + 'Cases_from_caseName.json') as file:
            file_dict=json.load(file)
        with open(base_dir + 'reduced_dictionary.json') as f:
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
                intersection = [value for value in list_cases_party_1 if value in list_cases_party_2]
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
                    if [file_dict[str(i[0])][j],float(i[1])/200] not in selected_cases:
                        selected_cases.append([file_dict[str(i[0])][j],float(i[1])/200])
                        count+=1
        else:
            selected_cases=selected_cases[:20]

        def sortSecond(val):
            return val[1]
        selected_cases.sort(key = sortSecond, reverse=True)
        # print(selected_cases)
        # d={}
        # for file in selected_cases:
            # d[file[0]]=file[1]
        d = []
        for x in selected_cases:
            d.append(x[0])
        final_dict = {}
        final_dict["acts"] = []
        final_dict["cases"] = d

        with open(base_dir + 'query_3.json','w') as out:
            json.dump(final_dict,out,indent=1)
    
    else:
        search_1=[]
        number_of_parties = 300
        party1 = query.split(' ')
        with open(base_dir + 'Cases_from_caseName.json') as file:
            file_dict=json.load(file)
        with open(base_dir + 'reduced_dictionary.json') as f:
            data = json.load(f)
        parties_1=[]

        for word in party1:
            # print(word[0])
            if word not in stop_words and word[0].isalpha():
                search_1.append(word[0].upper())
            if word.isupper():
                w=process.extract(word, d.keys(), limit=1, scorer=fuzz.token_set_ratio)
                for i in w:
                    w=d[i[0]]
                query=query.replace(word, w)
        count=0
        search_1 = set(search_1)
        search_1 = list(search_1)
        print(search_1)
        for k in search_1:
            parties_1 += process.extract(query, data[k], limit = number_of_parties, scorer=fuzz.token_set_ratio)
        selected_cases = []
        for i in parties_1:
            for j in range(len(file_dict[str(i[0])])):
                if count==20:
                    break
                if [file_dict[str(i[0])][j],float(i[1])/100] not in selected_cases:
                    selected_cases.append([file_dict[str(i[0])][j],float(i[1])/100])
                    count+=1
       
        d = []
        for x in selected_cases:
            d.append(x[0])
        final_dict = {}
        final_dict["acts"] = []
        final_dict["cases"] = d

        with open(base_dir + 'query_3.json','w') as out:
            json.dump(final_dict,out,indent=1)
    return final_dict
if __name__ == '__main__':

    q = input("Enter case : ")
    query_3(q)
    
    
