import csv
import re
import json




characteristicsArray = []
descriptionsArray = []
splitCharacteristics = []
descriptionsText = ''
descriptionsFile = open('ArchivoCompleto/descriptions.txt','r')
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
textoAux =''
for i in range(131):
	description = descriptionsArray[i][1]
	description = re.sub(r': ',':',description)
	decimales = []
	decimales = re.findall(r'\d\. ',description)
	for k in range(len(decimales)):
		description = description.replace(decimales[k],decimales[k].replace('. ','.'))
	decimales = re.findall(r'\d\.\d',description)
	for k in range(len(decimales)):
		description = description.replace(decimales[k],decimales[k].replace('.',','))
	characteristicsCount = 0
	for j in range(len(characteristicsArray)):
		coincidences = re.findall(r'('+characteristicsArray[j][0]+r'\s[\sa-zA-Z,;\(\)\-0-9\[\]:\+\?]*\.?\s)',description)
		if len(coincidences) != 0:
			characteristics[characteristicsArray[j][0]] = coincidences[0]
			insects[''+descriptionsArray[i][0]] = characteristics
	characteristics = {}
input = {"Especies":insects}
with open('data.json', 'w') as outfile:
    archivo = json.dump(input,outfile)

print(insects['Triatoma lecticularia']['Abdomen'])
i = 0
for i in range(len(characteristicsArray)):
	auxFile = open('CharValues/'+characteristicsArray[i][0]+'.txt','w')
	for j in insects:
		try:
			auxFile.write(j+'@'+insects[j][characteristicsArray[i][0]].replace(characteristicsArray[i][0]+' ','')+'\n')
		except KeyError: 
			print(j+ ' no tiene: '+characteristicsArray[i][0])