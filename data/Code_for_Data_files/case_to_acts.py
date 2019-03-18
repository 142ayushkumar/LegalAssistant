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


act_to_case_dict = {}
for i in range(len(cases)):
	for elem in cases[i]:
		if act_to_case_dict.has_key(elem.split('.')[0]):
			act_to_case_dict[elem.split('.')[0]].append(acts[i])
		else:
			act_to_case_dict[elem.split('.')[0]] = [acts[i]]

f1 = open('case_to_acts.json','w')
file = json.dumps(act_to_case_dict, indent  = 3)
f1.write(file)
