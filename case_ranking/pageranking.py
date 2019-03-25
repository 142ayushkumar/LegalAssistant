import json
import networkx as nx
import operator
base_dir = "/Users/saurav/Desktop/OpenSoft/OpenSoft-Data/"

with open(base_dir + 'case2.txt', 'r') as file:
	json_data = file.read()
	data = json.loads(json_data)
	# print(data)
	# print(type(data))


G = nx.DiGraph()

for k in data:
	for x in data[k]:
		# if x in 
		G.add_edge(k, x)


# print(len(data['2017_M_2']))

values = nx.pagerank(G, 0.85, None, 500000)
print(type(values))
values = sorted(values.items(), key=operator.itemgetter(1))
print(type(values))
case_to_score = dict()
for i in range(len(values)):
	case_to_score.update({values[i][0]:values[i][1]})

output = open(base_dir + 'case_ranking.txt', 'w')
json = json.dumps(case_to_score)
output.write(json)

# client.send(Message(text='Hello'), thread_id='142ayush', thread_type=ThreadType.USER)