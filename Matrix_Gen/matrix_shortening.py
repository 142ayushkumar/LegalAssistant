import json

fd = open("matrix.json")
data = json.load(fd)
fd.close()


fd1 = open("en_words.json")

word_dict = {}
for word in fd1:
	word_dict[word[:-1]] = 1
	
fd1.close()

new_dict = {}


for key in data:
	if key == "###":
		new_dict[key] = data[key]
		continue
	if key not in word_dict:
		continue
	c = 0
	for i in data[key]:
		c += i
	if c >500:
		new_dict[key] = data[key]

with open("new_matrix.json", "w") as write_file:
    json.dump(new_dict, write_file, sort_keys=True, indent=1)
