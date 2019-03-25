findMonth = {}

findMonth["January"] = 1
findMonth["February"] = 2
findMonth["March"] = 3
findMonth["April"] = 4
findMonth["May"] = 5
findMonth["June"] = 6
findMonth["July"] = 7
findMonth["August"] = 8
findMonth["September"] = 9
findMonth["October"] = 10
findMonth["November"] = 11
findMonth["December"] = 12

'''
date : Date in string form
Returns touple (year, month, day)
'''
def get_date(date) :
	_date = date.split()
	day = int(_date[0], 10)
	month = findMonth[_date[1]]
	year = int(_date[2], 10)
	return (year, month, day);

if __name__ == '__main__':
	q = input()
	print(get_date(q))