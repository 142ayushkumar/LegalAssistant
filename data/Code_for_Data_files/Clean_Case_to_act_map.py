
import re

with open("ActFreq.txt") as j:

	for line in j:
		line = re.sub('[^A-Za-z0-9 , :]+', '', line)
		print(line.rstrip(','))
