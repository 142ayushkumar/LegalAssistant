import json
from collections import OrderedDict
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from bing_spell_check_api import *

'''
query2(search_query) : Returns result in the form of dictionary in query2.json file 
'''

copy_rankings = {}

def cal(x):
	if x in copy_rankings:
		return -copy_rankings[x]
	else:
		return 0


def get_related_acts(search_query):

	file = open('actlist.txt' , 'r')

	abb_file = open('abbreviation_mapping.json', 'r')
	abb_dict = json.load(abb_file)
	acts = []
	
	tokenizer = RegexpTokenizer(r'\w+')
	act_tokens = tokenizer.tokenize(search_query)
	# print(act_tokens)

	numerical_part = []
	for word in act_tokens:
		if any(ch.isdigit() for ch in word):
			numerical_part.append(word)

	# print(numerical_part)



	for act in file:
		act = act.rstrip('\n')

		acts.append(act)
	for key in abb_dict:
		acts.append(key)

	file.close()

	# print(acts[:10])


	rel_acts = process.extract(search_query, acts, limit =50 ,scorer=fuzz.token_set_ratio)
	copy_rel_acts = []
	i = 0
	for act in rel_acts:
		if act[0] in abb_dict:
			for x in abb_dict[act[0]]:
				copy_rel_acts.append((x,act[1]))
		else :
			copy_rel_acts.append(act)
	# print(str(rel_acts) + '\n')

	return copy_rel_acts, numerical_part

def get_related_cases(rel_acts):
	

	f = open('act_to_cases.json','r')

	act_to_case_dict = json.load(f)
	cases = []
	for act in rel_acts:
		# print(act)
		try:
			for x in act_to_case_dict[act[0]]:
				cases.append(x)
		except :
			pass

	# print(set(cases))

	cases_relv = set(cases)
	
	return cases_relv



def query2(search_query):
	search_query = search_query.replace('.', '')

	search_query = corrected_text(search_query)

	rel_acts, numerical_part = get_related_acts(search_query)	

	final_dict = {}
	rel_acts_wo_score = [x[0] for x in rel_acts]
	final_dict['acts'] = rel_acts_wo_score[:min(10,len(rel_acts_wo_score))]
	# print(rel_acts)
	cases = get_related_cases(rel_acts)
	# print(cases)
	cases = list(cases)
	cases = cases[:min(10,len(cases))]
	# print(cases)
	f = open('case_ranking.json','r')
	rankings = json.load(f)
	# print(rankings[:10])

	scaling_ratio = 1000/6
	for key in rankings:
		copy_rankings[key] = rankings[key]*scaling_ratio


	sorted_cases = sorted(cases,key = lambda x:cal(x))
	cases_score_dict = {}
	# print(sorted_cases)
	for case in sorted_cases:
		if case in copy_rankings:
			cases_score_dict[case] = copy_rankings[case]
		else:
			cases_score_dict[case] = 0

	final_dict['cases'] = cases_score_dict

	f1 = open('query2.json','w')
	final = json.dumps(final_dict, indent = 1)
	f1.write(final)

if __name__ == '__main__':
	search_query = input("search query = ")
	query2(search_query)
