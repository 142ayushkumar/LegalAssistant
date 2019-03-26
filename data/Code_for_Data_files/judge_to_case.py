# Processes judge_to_case_unprocessed dict containing multiple juges in a single case
# and separates them.
# It also removes the words hon'ble,justice and J


import json
import collections
from collections import defaultdict

connectives = [" j ", " and "]
remove = ["hon ble", "justice"]

with open('judge_to_case_unprocessed.json') as json_file:  
    data = json.load(json_file)

def defV() :
	lst = []
	return lst
data_lower = defaultdict(defV)

for k, v in data.items() :
	data_lower[k.lower()] = data_lower[k.lower()] + v


final_0 = {k.replace(remove[0], ''): v for k, v in data_lower.items()}
final_1 = {k.replace(remove[1], ''): v for k, v in final_0.items()}
final_2 = {k.replace(' and ', ' j ') : v for k, v in final_1.items()}

st = set()
for v in final_2.keys() :
	for w in final_2[v] :
		st.add(w)
print(len(st))

final = {}
for judges, case in final_2.items() :
	judge_list = judges.split(' j ')
	for judge in judge_list : 
		if len(judge.replace(' ', '')) > 2 :
			if judge in final :
				final[judge.strip()] = final[judge] + case
			else :
				final[judge.strip()] = case


file = open('judge_to_case.json', 'w')
jp = json.dumps(collections.OrderedDict(sorted(final.items())), indent = 3)
file.write(jp)

