import json
import datetime
import operator
# from top_cases_given_labels import give_best_cases
import networkx as nx
# base_dir = "/Users/saurav/Desktop/OpenSoft/case_ranking/"

def give_best_cases(case_dict, label_names):
	'''
		In this function, give the input as a list of labels
		Note - the name of labels must match exactly with that in subject_to_case.txt
	'''

  #   with open('subject_to_case.txt', 'r') as file:
	 #    json_data = file.read()
		# category_data = json.loads(json_data)

	case_score = dict()
	# label_count = dict()

	for labels in label_names:
		try:
			with open(labels + '.txt', 'r') as file:
				json_data = file.read()
				label_data = json.loads(json_data)
		except:
			continue
		length = len(label_data)
		# Cases present in label_data
		for case in label_data:
			if case in case_dict:
				if case not in case_score:
					case_score[case] = 0
				else:
					case_score[case] = case_score[case] + label_data[case]*length

	# Assigning scores by using common citation graph
	with open('case_ranking.txt', 'r') as file:
		json_data = file.read()
		common_case_ranking = json.loads(json_data)

	length = len(common_case_ranking)
	for case in case_score:
		if case in common_case_ranking:
			case_score[case] = case_score[case] + common_case_ranking[case]*length


	# for case in case_score:
	#     label_count[case] = len(case_dict[case]['categories'])

	# If case in case_score, then it exist surely in case_dict
	case_score = sorted(case_score.items(), key = operator.itemgetter(1))

	case_score_list = []
	for case in case_score:
		case_score_list.append(case[0])

	case_score_list.sort(key = lambda z: case_dict[z]['value'])
	case_score_list.reverse()
		
	return case_score_list[:100]



def query_filter(query):

	fd1 = open('case_to_info.json')
	# fd2 = open('query.json')

	data = json.load(fd1)
	# query = json.load(fd2)


	fd1.close()
	# fd2.close()

	dict_of_values = {}


	from_d = query['from_date'].replace('/','')
	to_d = query['to_date'].replace('/','')

	for it in data:

		case_date = data[it]['date']
		case_date = case_date.replace('/','')
		# print(it)
		# print(from_d, to_d, case_date)
		if from_d <= case_date and to_d >= case_date and (not query['judge'] or data[it]['judges'][0] == query['judge']):
			list1 = []
			list2 = []
			# print('here')
			for cat in query["categories"]:
				if cat in data[it]["categories"]:
					list1.append(cat)

			for act in query["acts"]:
				if act in data[it]["acts"]:
					list2.append(act)

			if len(query['categories']) > 0 and len(list1) == 0:
				continue
			if len(query['acts']) > 0 and len(list2) == 0:
				continue

			val1 = len(list1)/max(1,len(query["categories"]))
			val2 = len(list2)/max(1,len(query["acts"]))

			temp_dict = {}
			temp_dict["category"] = list1
			temp_dict["acts"] = list2
			temp_dict["judge"] = query['judge']
			temp_dict["date"] = data[it]["date"]

			t = 2*val1*val2/max(1,val1+val2) + val1 + val2

			temp_dict["value"] = t
			# print(temp_dict)
			dict_of_values[it] = temp_dict

	unsorted_dict = {}

	for it in dict_of_values:
		unsorted_dict[it] = dict_of_values[it]["value"]

	sorted_dict = sorted(unsorted_dict.items(), key = operator.itemgetter(1), reverse =True) 
	# print(sorted_dict)
	sorted_final_dict = {}
	count = 0
	for it in sorted_dict:
		print(dict_of_values[it[0]]['value'])
		if count >= 1000:
			break
		sorted_final_dict[it[0]] = dict_of_values[it[0]]

		count += 1

	# print(sorted_final_dict)
	# jsonFile = json.dumps(dict_of_values)
	labels = query['categories']
	x = give_best_cases(sorted_final_dict, labels)
	return x

# if __name__ == '__main__':
# 	print(2)
	# fdh = open('query.json')
	# query = json.load(fdh)
	# # query_filter(query)
	# case_dict = query_filter(query)
	# labels = query['categories']
	# print(labels)
	# x = give_best_cases(case_dict, labels)
	# print(x)
