import json
import os

def case_to_date():

	f = open('case_to_date_format.json','r')
	case_to_date_dict = json.load(f)

	return case_to_date_dict


def case_to_judge():

	f = open('case_to_judge.json','r')
	case_to_judge_dict = json.load(f)

	return case_to_judge_dict
	


def case_to_acts():
	
	f = open('case_to_acts.json','r')
	case_to_act_dict = json.load(f)

	return case_to_act_dict

def case_to_categories():

	f1 = open('case_to_catchwords.json','r')
	dictn_1 = json.load(f1)

	f2 = open('case_to_subjects.json','r')
	dictn_2 = json.load(f2)


	case_to_categories_dict = {}
	lst = []

	for key in dictn_1.keys():
		for i in dictn_1[key]:
			lst.append(i)
		for i in dictn_2[key]:
			lst.append(i)
		case_to_categories_dict[key] = lst
		lst = []

	return case_to_categories_dict

def merge(case_to_act_dict, case_to_categories_dict, case_to_date_dict, case_to_judge_dict):

	final_dict = {}

	for key in case_to_date_dict:
		lst = {}

		try:
			lst['acts'] = case_to_act_dict[key]
		except:
			lst['acts'] = ''

		try:
			lst['categories'] = case_to_categories_dict[key]
		except:
			lst['categories'] = ''

		try:
			lst['date'] = case_to_date_dict[key]
		except:
			lst['date'] = ''

		try:
			lst['judges'] = case_to_judge_dict[key]
		except:
			lst['judges'] = ''

		final_dict[key] = lst
	
	return final_dict
		

if __name__ == '__main__':
	
		
	case_to_act_dict = case_to_acts()

	case_to_categories_dict = case_to_categories()

	case_to_date_dict = case_to_date()

	case_to_judge_dict = case_to_judge()

	final_dict = merge(case_to_act_dict, case_to_categories_dict, case_to_date_dict, case_to_judge_dict)

	file = open('case_to_info.json' , 'w')
	j = json.dumps(final_dict , indent = 3)
	file.write(j)