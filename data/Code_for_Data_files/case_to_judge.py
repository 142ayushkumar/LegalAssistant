import json

f = open('judge2caseID.json','r')

data = f.read()

data = data.replace('{','')
data = data.replace('}','')

data = data.split('],')

data1 = []
judges = []
for elem in data:
	judge, cases = elem.strip().strip('\n').split(':')
	judges.append(judge.strip("\""))
	cases = cases.strip().strip('[\n').strip().split(', \n      ')
	cases1 = []
	for case in cases:
		cases1.append(case.strip("\""))
	data1.append(cases1)

case_to_judge_dict = {}

for i in range(len(judges)):
	for case in data1[i]:
		if case_to_judge_dict.has_key(case):
			case_to_judge_dict[case.split('.')[0]].append(judges[i])
		else:
			case_to_judge_dict[case.split('.')[0]] = [judges[i]]

# print(judges[:3])
# print(data1[:3])

# print(case_to_judge_dict)

f1 = open('case_to_judge.json','w')
file = json.dumps(case_to_judge_dict, indent = 3)
f1.write(file)