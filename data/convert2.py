import os
import json

final_dict = {}
for subdir, dirs, files in os.walk("tf-idf-files"):
	for file_name in files:
		with open("tf-idf-files/" + file_name, 'r') as file:
			data=file.read().replace('\n', ' ')
			words = data.split()
			# print(words)
		final_dict[file_name[:-4]] = words
		
with open('file_to_words_tf_idf.json', 'w') as outfile:
		json.dump(final_dict, outfile)