import os
import json
acts_to_path = {}

path = 'OpenSoft-Data/Acts/Central_Text'
dirs = os.listdir('Central_Text')
os.chdir('Central_Text')
for folder in dirs:
    acts = os.listdir(folder)
    # path = path + '/' + folder
    os.chdir(folder)
    for file in acts:
        act = open(file,'r',encoding="utf8").read()
        act_info = act.split('_')
        acts_to_path[act_info[0]] = path + '/' + folder + '/' + file
    os.chdir('..')
os.chdir('..')

path = 'OpenSoft-Data/Acts/State_Text'
dirs = os.listdir('State_Text')
os.chdir('State_Text')
for folder in dirs:
    acts = os.listdir(folder)
    # path = path + '/' + folder
    os.chdir(folder)
    for file in acts:
        act = open(file,'r',encoding="utf8").read()
        act_info = act.split('_')
        acts_to_path[act_info[0]] = path + '/' + folder + '/' + file
    os.chdir('..')
os.chdir('..')

print(json.dumps(acts_to_path, indent = 2))
