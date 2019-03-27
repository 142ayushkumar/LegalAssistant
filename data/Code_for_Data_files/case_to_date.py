# Code for extracting dates from cases
# Folder used in this code : "All_FT" (Given with Problem Statement)
# Files generated in this code : "case_to_date.json"
# Functions used in this code are :
#	1.	case_to_date() :	Loads every text file in the folder 'All_FT' and extracts date from the text file and returns a dictionary case_to_date.


import json
import os

def case_to_date():

	file_names = os.listdir('All_FT')

	case_to_date_dict = {}
	i = 0
	for file in file_names:
		f1 = open('All_FT/'+file,'r')
		i = i + 1 
		date = f1.read().split('\n')[3].strip()
		file, w =file.split('.')
		case_to_date_dict[file] = date
		f1.close()
	
	return case_to_date_dict

if __name__ == '__main__':
	case_to_date_dict = case_to_date()


	file = open('case_to_date.json' , 'w')
	j = json.dumps(case_to_date_dict , indent = 3)
	file.write(j)
