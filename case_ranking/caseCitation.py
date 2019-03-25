import os
from collections import defaultdict
import pprint
import time
import json

start_time = time.time()
base_dir = "/Users/saurav/Desktop/OpenSoft/OpenSoft-Data/"


case = dict()
with open(base_dir + 'doc_path_ttl_id.txt', 'r') as file:
    lines = file.readlines()
    for cur_line in lines:
        words = cur_line.split('-->')
        if len(words)>2:
            case.update({words[2][0:-1]:words[0]})

# print(case)
# if s in case:
#     print(case[s])
os.chdir(base_dir)

store = defaultdict(list)

for subdir, dirs, files in os.walk("All_FT/"):
    for file in files:
        # print(file)
        x = open("All_FT/" + file, 'r')
        lines = x.readlines()
        # print(lines[0])
        file_id = file.split('.')     

        for cur_line in lines:
            words = cur_line.split(" ")
            # print(words)    
            for i in range(len(words)-2):
                word = words[i]
                if word.lower()=="indlaw":
                    # Form a string here
                    s = words[i-1][-4:] + " " + words[i] + " " + words[i+1] + " "
                    numbers = '0123456789'
                    last_word = ''
                    for c in words[i+2]:
                        if c in numbers:
                            last_word += c
                    s += last_word 

                    if s in case:
                        store[file_id[0]].append(case[s])            
        store[file_id[0]] = list(set(store[file_id[0]]))
        x.close()
        # break

output = open(base_dir + 'case2.txt', 'w')
json = json.dumps(store)
output.write(json)



print("--- %s seconds ---" % (time.time() - start_time))