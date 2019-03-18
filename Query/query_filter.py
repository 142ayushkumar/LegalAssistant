import json
import datetime
fd1 = open('final_dictionary.json')
fd2 = open('query.json')

data = json.load(fd1)
query = json.load(fd2)


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
		temp_dict["value"] = val1*val2*val3/max(1,val1*val2 + val2*val3 + val3*val1) + val1 + val2 + val3

		dict_of_values[it] = temp_dict

for dd in dict_of_values:
	if dict_of_values[dd]["value"]>1.6:
		print(dict_of_values[dd])
jsonFile = json.dumps(dict_of_values)