import re
from nltk.corpus import stopwords
import json
from collections import OrderedDict
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
import sys
sys.path.insert(0, '../')
from bing_spell_check_api import *
stop_words = set(stopwords.words('english'))
base_dir = ''

def cal(x, copy_rankings):
	if x in copy_rankings:#.has_key(x):
		return -copy_rankings[x]
	else:
		return 0


def get_related_acts(search_query):

	file = open(base_dir + 'actlist.txt' , 'r')

	abb_file = open(base_dir + 'abbreviation_mapping.json', 'r')
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
		if act[0] in abb_dict:#.has_key(act[0]):
			for x in abb_dict[act[0]]:
				copy_rel_acts.append((x,act[1]))
		else :
			copy_rel_acts.append(act)
	# print(str(rel_acts) + '\n')

	return copy_rel_acts, numerical_part

def get_related_cases(rel_acts):
	

	f = open(base_dir + 'act_to_cases.json','r')

	act_to_case_dict = json.load(f)
	cases = []
	for act in rel_acts:
		# print(act)
		try:
			for x in act_to_case_dict[act[0]]:
				cases.append(x)
		except :
			pass

	# print(cases[0])

	cases_relv = set(cases)
	# print(cases_relv)
	return cases_relv



def cases_and_acts(search_query):
	# search_query = raw_input("search query = ")
	search_query1 = search_query.replace('.', '')

	try:
		search_query = corrected_text(search_query1)
	except:
		search_query = search_query1

	rel_acts, numerical_part = get_related_acts(search_query)	

	final_dict = {}
	rel_acts_wo_score = [x[0] for x in rel_acts]
	final_dict['acts'] = rel_acts_wo_score[:min(10,len(rel_acts_wo_score))]
	# print(rel_acts)
	cases = get_related_cases(rel_acts)
	cases = list(cases)
	cases = cases[:min(10,len(cases))]
	# print(cases)
	# print(cases)
	f = open(base_dir + 'case_ranking.json','r')
	rankings = json.load(f)
	# print(rankings[:10])
	copy_rankings = {}
	scaling_ratio = 1000/6
	for x in rankings:
		# print(i)
		copy_rankings[x] = rankings[x]*scaling_ratio
	# print(copy_rankings)

	sorted_cases = sorted(cases, key = lambda x:cal(x, copy_rankings))
	# print("Here")
	# for i in range(0, len(sorted_cases)):
	# 	print(sorted_cases[i], cal(sorted_cases[i], copy_rankings))
	# print("Here")

	final_dict['cases'] = sorted_cases

	return final_dict
# inp_words = input()

def act_query(inp_words = "State of Maharashtra vs Ayush"):

	inp_words = re.split(' |, |-|\(|\)', inp_words)

	flag_sec = 0
	flag = 0
	sec_no = "-1"
	year = "-1"
	str_acts = ""

	for i in range(len(inp_words)):
		if inp_words == "":
			continue

		if inp_words[i][0] >= '0' and inp_words[i][0] <= '9' and len(inp_words[i]) == 4:
			year = inp_words[i]
			continue

		if flag == 0:
			if inp_words[i].lower() == "sec" or inp_words[i].lower() == \
				"sect" or inp_words[i].lower() == "secti" or inp_words[i].lower() == \
				"sectio" or inp_words[i].lower() == "section":

				flag = 1


			elif inp_words[i].lower() not in stop_words:
				str_acts += " "
				str_acts += inp_words[i]

		elif flag == 2 and inp_words[i].lower() not in stop_words:

			str_acts += " "
			str_acts += inp_words[i]

		elif inp_words[i][0] >= '0' and inp_words[i][0] <= '9':
			flag = 2
			sec_no = inp_words[i]

	if sec_no != '-1':
		sec_no = int(sec_no)

	if year != "-1":
		year = int(year)

	final_dict = cases_and_acts(str_acts[1:])

	final_dict["section"] = sec_no

	final_dict["year"] = year
	with open(base_dir + 'query_2.json','w') as out:
            json.dump(final_dict,out,indent=1)
	return final_dict

