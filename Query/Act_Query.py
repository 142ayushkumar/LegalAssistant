import re

inp_words = input()

# flag = 0
# for i in range(len(inp_words)-1, -1, -1):
# 	if flag == 0 and inp_words[i] == '\)':
# 		del inp_words[i]
# 		flag = 1
# 	if flag == 1 and inp_words[i] == '\(':
# 		del inp_words[i]
# 		flag = 0
# 	if flag == 1:
# 		del inp_words[i]
# print(inp_words)

inp_words = re.split(' |, |,|-', inp_words)

flag = 0

for i in range(len(inp_words)):
	if inp_words == "":
		continue
	if inp_words[i][0] >= '0' and inp_words[i][0] <= '9':
		flag = 1
		section_no = inp_words[i]
		flag_here = 0
		for j in range(len(inp_words)):
			if (inp_words[j].lower() == "sec" or inp_words[j].lower() == \
				"sect" or inp_words[j].lower() == "secti" or inp_words[j].lower() == \
				"sectio" or inp_words[j].lower() == "section"):
				flag_here = 1
				break

		for k in range(max(i,j),min(i,j)-1, -1):
			del inp_words[k]
		break

if flag == 0:
	print("No sections given")
else:
	print("Act: ", end = "")

	for i in inp_words:
		# print(i)
		if i == "" or (i[0] >= '0' and i[0] <= '9'):
			continue
		print(i, end = " ")

	print("\nSection: " + section_no)