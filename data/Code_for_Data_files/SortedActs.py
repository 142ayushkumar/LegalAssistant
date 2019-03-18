
import re


with open("Actnumber.txt") as j:
	for line in sorted(j, key=lambda line: int(line.split(":")[1])):
		print(line)
