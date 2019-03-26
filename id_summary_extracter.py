from bs4 import BeautifulSoup
import os
import json

c_file = open('data/file_to_date_casename_casecode_judge_judgment.json','r')
case_to_casename_dict = json.load(c_file)

basic_path = '/home/taral/Documents/opensoft19/summary/'

files = os.listdir('/home/taral/Documents/opensoft19/summary/')
case_summ_dict  = {}
for file in files:
	i = 0
	f1 = open(basic_path + file, 'r')
	soup = BeautifulSoup(f1,'html.parser')
	case_id = [] 	
	case_sum = []
	summary = soup.find_all('bound')

	for x in summary:
		if i==0:
			if case_to_casename_dict[file.split('.')[0]][1].startswith(x.text):
				i = 1
			else:
				break
		try:
			if isdigit(x.attrs['id']):
				case_id.append(x.attrs['id'])
			else:
				continue
		except Exception as e:
			continue
		case_sum.append(x.text)
	case_summ_dict[file.split('.')[0]] = [case_sum,case_id]

f = open('case_summary_with_id.json', 'w')
final = json.dumps(case_summ_dict, indent  = 1)
f.write(final)