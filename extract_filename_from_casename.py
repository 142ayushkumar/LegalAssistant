import json
d={}
S={""}
f=open("CaseNames.txt","a+")
lines=[line.rstrip('\n') for line in open('doc_path_ttl_id.txt')]
for line in lines:
	case=line.split('-->')
	print(case[1])
	case[1]=case[1].strip()
	case[1]=case[1].decode("utf-8")
	case[1]=case[1].replace(u"\u2019"," ")
	case[1]=case[1].encode('ascii','ignore')
	if case[1].find(' v ')>=0:
		[c1,c2]=case[1].split(' v ')
		c1=c1.lstrip(" ")
		print(type(c1))
		S.add(c1)
		#f.write(case[1])
		#f.write('\n')
		c2=c2.lstrip(" ")
		S.add(c2)
		print(type(c2))
		d.setdefault(c1, []).append(case[0])
		d.setdefault(c2, []).append(case[0])
	else:
		c1=case[1]
		print(type(c1))
		S.add(c1)
		#f.write(case[1])
		#f.write('\n')
		d.setdefault(c1, []).append(case[0])
print(type(d))
for i in S:
	f.write(i)
	f.write('\n')
f.close()
with open('Cases_from_caseName.json','w') as out:
	json.dump(d,out) 
