import re

def(file_name, list_of_acts):
	all_words = []
	fd = open(file_name)

	for line in fd:
		temp_words = re.split(',| ', line)
		for word in temp_words:
			if word != "":
				all_words.append(word)

	segment_index = []
	for i in range(len(all_words)):
		if all_words[i][:-3] == "-->":
			segment_index.append(i)
	caseName_index = []

	line_no = 0
	for line in fd:
		for act in list_of_acts:

			offset = 0

			while line[offset].find(act) != -1:
				pos = line[offset].find(act)
				caseName_index.append((line_no, offset+pos, len(act)))
				offset = offset + pos

		line_no++

	return segment_index, caseName_index

if __init__ == "__main__":
	inp = input()

