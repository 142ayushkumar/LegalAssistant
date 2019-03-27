import json
import datetime
import operator


def filter_query(list_of_cases, query):

	fd1 = open('final_dictionary.json')
	# fd2 = open('query.json')
	fd3 = open('case_ranking.json')
	# fd4 = open('list_of_cases.txt')
	fd5 = open('case_to_acts.json')

	data = json.load(fd1)
	# query = json.load(fd2)
	case_ranking = json.load(fd3)
	# list_of_cases = json.load(fd4)
	case_to_acts = json.load(fd5)


	fd1.close()
	# fd2.close()
	fd3.close()
	fd5.close()

	dict_of_values = {}


	for it in list_of_cases:
		# it = it[:-1]
		if it not in data:
			continue
		# print(it)
		if 1:#it.date >= query.from_fate and it.date <= query.to_date:
			list1 = []
			list2 = []
			list3 = []

			for cat in query["categories"]:
				if cat in data[it]["categories"]:
					list1.append(cat)

			for act in query["acts"]:
				if act in data[it]["acts"]:
					list2.append(act)

			for judge in query["judges"]:
				if judge in data[it]["judges"]:
					list3.append(judge)

			val1 = len(list1)/max(1,len(query["categories"]))
			val2 = len(list2)/max(1,len(query["acts"]))
			val3 = len(list3)/max(1,len(query["judges"]))

			temp_dict = {}
			temp_dict["category"] = list1
			temp_dict["acts"] = list2
			temp_dict["judges"] = list3
			temp_dict["date"] = data[it]["date"]
			if it in case_to_acts:
				temp_dict["acts"] = case_to_acts[it]
			t = 3*val1*val2*val3/max(1,val1*val2 + val2*val3 + val3*val1) + val1 + val2 + val3
			u = 0
			if(it in case_ranking):
				u = 1e3*case_ranking[it]
			temp_dict["value"] = 2*t*u/max(1, t + u) + t + u
			dict_of_values[it] = temp_dict

	unsorted_dict = {}
	for it in dict_of_values:
		unsorted_dict[it] = dict_of_values[it]["value"]

	sorted_dict = sorted(unsorted_dict.items(), key = operator.itemgetter(1), reverse =True) 

	sorted_final_dict = {}

	for it in sorted_dict:
		sorted_final_dict[it] = dict_of_values[it[0]]

	# print(sorted_final_dict)
	# jsonFile = json.dumps(dict_of_values)
	# fd4.close()
	return sorted_final_dict
