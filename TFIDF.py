import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import json
stop_words = set(stopwords.words('english'))
import math

if __name__ == "__main__":
	mainFile = open("subject_to_case.json", "r")
	data = {}
	data = json.load(mainFile)

	for key in data :
		
		totalCountOfWords = dict()
		numberOfDocuments = dict()
		Tfidf = []

		key = "criminal"

		print(key)

		cnt = 0

		for case in data[key] :
			
			if cnt > 100:
				break

			cnt += 1

			location = "H:\\Downloads\\OpenSoft-Data\\OpenSoft-Data\\All_FT\\"
			location = location + str(case) + ".txt"
			tempFile = open(location, "r")

			print(location)

			check = dict()

			for line in tempFile:
				for word in line.split():
					val = word.lower()
					fin = ""
					key1 = False
					
					for char in val:
						if char >= 'a' and char <= 'z':
							fin = fin + char
						elif char >= '0' and char <= '9':
							key1 = True
							break

					if key1 == True:
						continue

					if fin == "":
						continue
					
					if fin not in stop_words and fin != "":
						if fin in totalCountOfWords:
							totalCountOfWords[fin] += 1
						else :
							totalCountOfWords[fin] = 1

						check[fin] = 1

			for word in check:
				if word in numberOfDocuments:
					numberOfDocuments[word] += 1
				else :
					numberOfDocuments[word] = 1


		V = dict()
		cnt = 0
		key = "criminal"

		for case in data[key]:

			if cnt > 100:
				break

			cnt += 1

			count = dict()
			totalNumberOfWords = 0
			location = "H:\\Downloads\\OpenSoft-Data\\OpenSoft-Data\\All_FT\\"
			location = location + str(case) + ".txt"
			tempFile = open(location, "r")

			for line in tempFile:
				for word in line.split():
					val = word.lower()
					fin = ""
					key1 = False
					
					for char in val:
						if char >= 'a' and char <= 'z':
							fin = fin + char
						elif char >= '0' and char <= '9':
							key1 = True
							break

					if key1 == True:
						continue

					if fin == "":
						continue

					if fin not in stop_words and fin != "":
						if fin in count:
							count[fin] += 1
						else :
							count[fin] = 1
						totalNumberOfWords += 1


			for word in count:
				Tf = count[word] / totalNumberOfWords
				IDF = math.log(len(data[key]) / numberOfDocuments[word])
				if word in V:
					V[word] = max(V[word], Tf*IDF)
				else :
					V[word] = Tf*IDF


		for word in V:
			Tfidf.append((V[word], word))

		Tfidf.sort(reverse = True)
		
		for i in range(0, 1000):
			print(Tfidf[i])

		break


			
