import csv
import re
import json
characteristicsArray = []
descriptionsArray = []
splitCharacteristics = []
descriptionsText = ''
descriptionsFile = open('C:\\Users\\bryan\\Documents\\Github\\Filogenia-Triatominae\\ArchivoCompleto\\descriptions.txt','r')
descriptionsText = descriptionsFile.read();
splitDescriptions = descriptionsText.split('\n')
for i in range(len(splitDescriptions)):
	descriptionsArray.append(splitDescriptions[i].split('@'))

with open('insectsCharacteristics.csv', newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        characteristicsArray.append(row)
insects={}
characteristics = {}
for i in range(26):
	description = descriptionsArray[i][1]
	characteristicsCount = 0
	for j in range(len(characteristicsArray)):
		coincidences = re.findall(r'('+characteristicsArray[j][0]+r'\s[\sa-zA-Z,;\(\)\-0-9\[\]:\+\?]*\.?)',description)
		if len(coincidences) != 0:
			characteristics[characteristicsArray[j][0]] = coincidences[0]
			insects[''+descriptionsArray[i][0]] = characteristics
input = {"Especies":insects}
with open('data.json', 'w') as outfile:
    archivo = json.dump(input,outfile)