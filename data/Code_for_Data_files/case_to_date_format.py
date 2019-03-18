import json
import os

def month_to_number(strn):


	if strn == 'January':
		strn = '01'
		return strn

	if strn == 'February':
		strn = '02'
		return strn
	
	if strn == 'March':
		strn = '03'
		return strn

	if strn == 'April':
		strn = '04'
		return strn

	if strn == 'May':
		strn = '05'
		return strn

	if strn == 'June':
		strn = '06'
		return strn

	if strn == 'July':
		strn = '07'
		return strn

	if strn == 'August':
		strn = '08'
		return strn

	if strn == 'September':
		strn = '09'
		return strn

	if strn == 'October':
		strn = '10'
		return strn

	if strn == 'November':
		strn = '11'
		return strn

	if strn == 'December':
		strn = '12'
		return strn

	return strn
	

def case_to_date():

	with open('case_to_date.json', 'r') as f:
		case_to_date_dict = json.load(f)
	return case_to_date_dict


if __name__ == '__main__':
	case_to_date_dict = case_to_date()


	for key in case_to_date_dict:
		lst = case_to_date_dict[key].split(' ')


		lst[1] = month_to_number(lst[1])

		try:
			if int(lst[0]) < 10:
				lst[0] = '0' + lst[0]
		except:
			pass
		
		case_to_date_dict[key] = lst[2]+'/'+lst[1]+'/'+lst[0] 

	c = 0
	for key in case_to_date_dict:
		if c < 10:
			print(key, case_to_date_dict[key])
		c = c + 1

	file = open('case_to_date_format.json' , 'w')
	j = json.dumps(case_to_date_dict , indent = 3)
	file.write(j)