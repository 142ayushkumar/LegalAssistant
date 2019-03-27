# Code for generating dates of cases in the following format : YYYY/MM/DD
# Files used in this code : "case_to_date.json"
# Files generated in this code : "case_to_date_format.json"
# Functions used in this code are :
#	1.	month_to_number() :	Takes a month and converts it to its respective number.
#							For example 'January' gets converted to '01'
#	2.	date_to_proper_format() :	Converts a given case_to_date dictionary into required date format(YYYY/MM/DD). 
#									For example "2000 04 06" gets coverted to "2000/04/06"



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

def date_to_proper_format(case_to_date_dict):

	for key in case_to_date_dict:
		lst = case_to_date_dict[key].split(' ')


		lst[1] = month_to_number(lst[1])

		try:
			if int(lst[0]) < 10:
				lst[0] = '0' + lst[0]
		except:
			pass
		
		case_to_date_dict[key] = lst[2]+'/'+lst[1]+'/'+lst[0] 

	return case_to_date_dict


if __name__ == '__main__':

	with open('case_to_date.json', 'r') as f:
		case_to_date_dict = json.load(f)
	
	case_to_date_dict = date_to_proper_format(case_to_date_dict)					

	file = open('case_to_date_format.json' , 'w')
	j = json.dumps(case_to_date_dict , indent = 3)
	file.write(j)
