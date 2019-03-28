import json
import networkx as nx
import operator
# base_dir = "/Users/saurav/Desktop/OpenSoft/case_ranking/"

with open('subject_to_case.txt', 'r') as file:
	json_data = file.read()
	category_data = json.loads(json_data)

def give_best_cases(label_names):
	'''
		In this function, give the input as a list of labels
		Note - the name of labels must match exactly with that in subject_to_case.txt
	'''
	case_score = dict()
	label_count = dict()
	for labels in label_names:
		# print(labels)
		for cases in category_data[labels]:
			case_score[cases] = 0
			if cases not in label_count:
				label_count[cases] = 1;
			else:
				label_count[cases] = label_count[cases] + 1;

	for labels in label_names:
		with open(labels + '.txt', 'r') as file:
			json_data = file.read()
			label_data = json.loads(json_data)
		for case in label_data:
			case_score[case] = case_score[case] + label_data[case]*len(label_data) 

	case_score = sorted(case_score.items(), key = operator.itemgetter(1))
	case_score.sort(key = lambda z: label_count[z[0]])
	case_score.reverse()
	return case_score[:100]

if __name__ == '__main__':
	n = int(input("Number of Categories"))
	label_names = []
	for i in range(n):
		label = input("Give Category")
		label_names.append(label)
	# print(label_names)
	x = []
	x = give_best_cases(label_names)
	print(x)
