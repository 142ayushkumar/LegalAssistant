import json
import networkx as nx
import operator
base_dir = "/Users/saurav/Desktop/OpenSoft/OpenSoft-Data/"

with open(base_dir + 'case2.txt', 'r') as file:
	json_data = file.read()
	data = json.loads(json_data)
	# print(data)
	# print(type(data))


G = nx.Graph()

for k in data:
	for x in data[k]:
		G.add_edge(k, x)


# print(data['2017_M_2'])

values = nx.pagerank(G, 0.05, None, 50000)
values = sorted(values.items(), key=operator.itemgetter(1))

for i in range(-10, 0):
	print(values[i][0], values[i][1])
