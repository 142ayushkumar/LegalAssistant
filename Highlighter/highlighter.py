import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))


def highlighter_function(file_name, list_of_acts_file):
	all_words = []
	fd = open(file_name)
	fd2 = open(list_of_acts_file)

	all_acts = []

	for line in fd2:
		if line != '\n' and line!= "":
			# print(len(line[:-1]))
			all_acts.append(line[:-1])

	segment_index = []
	caseName_index = []

	line_no = 0

	for line in fd:
		temp_words = re.split(', | |\. |\.', line)

		for word_no in range(len(temp_words)):
			if temp_words[word_no][-3:] =="-->":
				segment_index.append((line_no, word_no))

		for word_no in range(len(temp_words)):
			
			if temp_words[word_no] == "Act" and word_no <= len(temp_words)-2:
				if word_no + 2 >= len(temp_words) or temp_words[word_no+2][-3:] != "-->":
					
					char = temp_words[word_no+1][0]
					
					if char >= '0' and char <= '9':
						start_word = word_no

						flag = 0
						while start_word >= 0:
							start_word -= 1
							# print(line_no, temp_words[start_word])
							if flag == 0 and temp_words[start_word] in stop_words:
								start_word += 1
								break
							elif flag == 0 and temp_words[start_word][-1] == ')':
								flag = 1
							elif flag == 1 and temp_words[start_word][0] == '(':
								flag = 0
							
						caseName_index.append((line_no, start_word, word_no+1))

		line_no += 1


	print(segment_index)
	print(caseName_index)

	return segment_index, caseName_index

if __name__ == "__main__":

	highlighter_function("Act.txt", "all_acts_central_state.txt")