import json

fd = open("abbreviation_mapping.json")

data = json.load(fd)
fd.close()

new_dict = {}
str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for char in str:
	new_dict[char] = []


for key in data:
	for char in key:
		if char in str:
			for cases in data[key]:
				new_dict[char].append(cases)

with open("char_to_cases.json", "w") as write_file:
    json.dump(new_dict, write_file, sort_keys=True, indent=1)

for char in new_dict:
	print(len(new_dict[char]))