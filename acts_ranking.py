import json

if __name__ == "__main__":
	caseRankingFile = open("C:\\emacs\\opensoft19\\data\\case_ranking.json", "r")
	caseRanking = json.load(caseRankingFile)

	caseToActsFile = open("C:\\emacs\\opensoft19\\data\\case_to_acts.json", "r")
	caseToActs = json.load(caseToActsFile)

	totalValue = dict()

	for case in caseToActs:
		val = 0
		if case in caseRanking:
			val = caseRanking[case]
		for acts in caseToActs[case]:
			if acts in totalValue:
				totalValue[acts] += val
			else:
				totalValue[acts] = val


	allActs = []
	for acts in totalValue:
		allActs.append((totalValue[acts], acts))

	totalActsFile = open("C:\\emacs\\opensoft19\\data\\actlist.json", "r")

	for line in totalActsFile:
		line = line.strip()
		line = line.replace('"', '')
		if line not in totalValue:
			allActs.append((0, line))

	allActs.sort(reverse = True)

	actsToRank = dict()

	for i in range(0, len(allActs)):
		actsToRank[allActs[i][1]] = allActs[i][0]


	with open('acts_ranking.json', 'w') as outfile:
		json.dump(actsToRank, outfile)