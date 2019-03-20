import json
import datetime
import operator
fd1 = open('final_dictionary.json')
fd2 = open('query.json')
fd3 = open('case_ranking.json')

data = json.load(fd1)
query = json.load(fd2)
case_ranking = json.load(fd3)

fd1.close()
fd2.close()

dict_of_values = {}


for it in data:
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
		t = 3*val1*val2*val3/max(1,val1*val2 + val2*val3 + val3*val1) + val1 + val2 + val3
		u = 0
		if(it in case_ranking):
			u = 1e3*case_ranking[it]
		temp_dict["value"] = 2*t*u/max(1, t + u) + t + u
		dict_of_values[it] = temp_dict


sorted_list = sorted(dict_of_values.items(), key=lambda k: dict_of_values[k]["value"] )
print(dict_of_values)
for i, key in zip(range (50), sorted_list):
	print(key)

# jsonFile = json.dumps(dict_of_values)