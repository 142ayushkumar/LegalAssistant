import json

f = open('output','r')

data = f.read()

w, data = data.split('{')
data, w = data.split('}')

data = data.split('],')

acts = []
cases = []
data1 = []

for elem in data:
	data1.append(elem.strip('\n').strip())

for elem in data1:
	act, case = elem.split(': ')
	acts.append(act.strip("\'"))
	case = case.strip('[')
	case_list = case.split(',\n')
	case_list1 = []
	for elem in case_list:
		case_list1.append(elem.strip().strip("\'"))
	cases.append(case_list1)


case_to_act_dict = {}
for i in range(len(cases)):
	for elem in cases[i]:
		if case_to_act_dict.has_key(elem.split('.')[0]):
			case_to_act_dict[elem.split('.')[0]].append(acts[i])
		else:
			case_to_act_dict[elem.split('.')[0]] = [acts[i]]

for elem in case_to_act_dict:
	case_to_act_dict[elem] = list(set(case_to_act_dict[elem]))

f1 = open('case_to_acts.json','w')
file = json.dumps(case_to_act_dict, indent  = 3)
f1.write(file)
