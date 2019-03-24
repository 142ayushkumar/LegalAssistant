import json
from collections import defaultdict

def defaultValue():
	lst=[]
	for i in range(len(labels)):
		lst.append(0)
	return lst


with open('../file_to_words.json') as fp: # file to words with frequency dict
    d = json.load(fp)

with open('catagories.json') as fp:   # list of labels
    catagories = json.load(fp)

with open('case_catagories.json') as fp: # Case to labels dict
    case_labels = json.load(fp)

labels=sorted(catagories.keys())

#labels.append("zN")
labels.append(0)

mat= defaultdict(defaultValue)
mat['###']=labels

index={}

for i in range(len(labels)):
	index[labels[i]]=i

zz=0
for file,word in d.items():
	# zz= zz+1
	# print "Processed ", (zz*100.0) / len(d.keys()), "%"
	for word,freq in d[file].items():
		file_name=file[:-4]
		try:
			for label in case_labels[file_name]:
				mat[word][index[label]] = mat[word][index[label]]+freq		

		except:
			continue

		

for k in mat.keys():
	c=0
	for i in mat[k]:
		if i !=0:
			c=c+1
	mat[k][len(mat[k])-1]=c




with open('matrix.json', 'w') as fp:
	json.dump(mat, fp, sort_keys=True, indent=1)







