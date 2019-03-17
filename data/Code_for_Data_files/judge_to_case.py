import json
import collections

connectives = [" j ", " and "]
remove = ["hon ble", "justice"]

with open('../judge_to_case_unprocessed.json') as json_file:  
    data = json.load(json_file)

data_lower =  {k.lower(): v for k, v in data.items()} # change to lower case 

final_0 = {k.replace(remove[0], ''): v for k, v in data_lower.items()}
final_1 = {k.replace(remove[1], ''): v for k, v in final_0.items()}
final_2 = {k.replace(' and ', ' j ') : v for k, v in final_1.items()}

final = {}
for judges, case in final_2.items() :
	judge_list = judges.split(' j ')
	for judge in judge_list : 
		if len(judge.replace(' ', '')) > 2 :
			if judge in final :
				final[judge.strip()] = final[judge] + case
			else :
				final[judge.strip()] = case


file = open('../judge_to_case.json', 'w')
jp = json.dumps(collections.OrderedDict(sorted(final.items())), indent = 3)
file.write(jp)

