import json
import os
file_names = os.listdir('CaseDocuments/All_FT')

case_to_date_dict = {}
i = 0
for file in file_names:
	f1 = open('CaseDocuments/All_FT/'+file,'r')
	data = f1.read()
	i = i + 1 
	print(i)
	date = data.split('\n')[3].strip()
	if not date[0].isdigit() :
		date = data.split('\n')[5].strip()
	case_to_date_dict[file.split('.')[0]] = date
	f1.close()

# print(case_to_date_dict)

f1 = open('case_to_date.json','w')

dictionary = json.dumps(case_to_date_dict, indent = 3)
f1.write(dictionary)