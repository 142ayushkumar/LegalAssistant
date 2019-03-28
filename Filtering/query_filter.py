import json
import datetime
import operator


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

	return sorted_final_dict

if __name__ == '__main__':
	
	fdh = open('query.json')
	query = json.load(fdh)
	# query_filter(query)
	print(query_filter(query))