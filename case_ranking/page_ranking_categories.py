import json
import networkx as nx
import operator
base_dir = ""

with open(base_dir + 'subject_to_case.txt', 'r') as file:
	json_data = file.read()
	category_data = json.loads(json_data)


with open(base_dir + 'case2.txt', 'r') as file:
	json_data = file.read()
	data = json.loads(json_data)
	# print(data)
	# print(type(data))

for key in category_data:
	G = nx.DiGraph()
	for k in data:
		for x in data[k]:
			if x in category_data[key] and k in category_data[key]: 
				G.add_edge(k, x)

	values = nx.pagerank(G, 0.85, None, 500000)
	# print(type(values))
	values = sorted(values.items(), key=operator.itemgetter(1))
	# print(type(values))
	print(values)
	case_to_score = dict()
	for i in range(len(values)):
		case_to_score.update({values[i][0]:values[i][1]})

	output = open(base_dir + 'case_ranking/' + key +  '.txt', 'w')
	print(type(case_to_score))
	js = json.dumps(case_to_score)
	output.write(js)
	print(key)
