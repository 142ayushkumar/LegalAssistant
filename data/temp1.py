import json

with open('file_to_date_casename_casecode_judge_judgment.json') as file:
	json_data = file.read()
	code_to_file = json.loads(json_data)



with open('caseCitations.txt', 'r') as file:
	json_data = file.read()
	data = json.loads(json_data)


for key in data:
	length = len(data[key])
	new_list = []
	for i in range(0, length):
		if data[key][i] in code_to_file:
			new_list.append(code_to_file[data[key][i]][1])
	data[key] = new_list

output = open('caseCitationsName.txt', 'w')
js = json.dumps(data)
output.write(js)
