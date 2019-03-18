import os
from collections import defaultdict
import pprint
import time
from termcolor import colored

start_time = time.time()
base_dir = "/Users/saurav/Desktop/OpenSoft/OpenSoft-Data/"

case_name = set()

with open(base_dir + 'doc_path_ttl_id.txt', 'r') as file:
    lines = file.readlines()
    for cur_line in lines:
        words = cur_line.split('-->')
        if len(words)>1:
            case_name.add(words[2][:-1])

# print(case_name)

act_name = set()

with open(base_dir + 'actlist.txt', 'r') as file:
    lines = file.readlines()
    for cur_line in lines:
        words = cur_line.split(',')
        if len(words)>1:
            act_name.add(words[-2])

os.chdir(base_dir)

for subdir, dirs, files in os.walk("All_FT/"):
    for file_name in files:
        word_list = []
        with open(base_dir + "All_FT/" + file_name, 'r') as file:
            data=file.read().replace('\n', ' ')
        words = data.split()
        length = len(words)
        for i in range(length):
            for j in range(1,20):
                if i+j<length:
                    s = words[i]
                    for k in range(1,j):
                        s += " " + words[i+k]
                    if s in case_name:
                        if i!=0:
                            print(s)
                            # print(i,i+j)
        file.close()
        # break
        # print(word_list)


print("--- %s seconds ---" % (time.time() - start_time))
