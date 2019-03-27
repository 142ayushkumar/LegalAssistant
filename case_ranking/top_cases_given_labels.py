import json
import networkx as nx
import operator
# base_dir = "/Users/saurav/Desktop/OpenSoft/case_ranking/"

def give_best_cases(case_dict, label_names):
	'''
		In this function, give the input as a list of labels
		Note - the name of labels must match exactly with that in subject_to_case.txt
	'''

  #   with open('subject_to_case.txt', 'r') as file:
	 #    json_data = file.read()
		# category_data = json.loads(json_data)

	case_score = dict()
	# label_count = dict()

	for labels in label_names:
		with open(labels + '.txt', 'r') as file:
			json_data = file.read()
			label_data = json.loads(json_data)
		length = len(label_data)
		# Cases present in label_data
		for case in label_data:
			if case in case_dict:
				case_score[case] = case_score[case] + label_data[case]*length

	# Assigning scores by using common citation graph
	with open('case_ranking.txt', 'r') as file:
		json_data = file.read()
		common_case_ranking = json.loads(json_data)

	length = len(common_case_ranking)
	for case in case_score:
		if case in common_case_ranking:
			case_score[case] = case_score[case] + common_case_ranking[case]*length


	# for case in case_score:
	#     label_count[case] = len(case_dict[case]['categories'])

	case_score = sorted(case_score.items(), key = operator.itemgetter(1))
	case_score.sort(key = lambda z: case_dict[z]['value'])
	case_score.reverse()
		
	return case_score[:100]

if __name__ == '__main__':
	n = int(input("Number of Categories"))
	label_names = []
	for i in range(n):
		label = input("Give Category")
		label_names.append(label)
	print(label_names)
	x = []
	x = give_best_cases(label_names)
	print(x)
