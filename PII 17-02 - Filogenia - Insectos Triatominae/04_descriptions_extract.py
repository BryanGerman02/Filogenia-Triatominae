#Sistema semiautomático para la extracción de las descripciones de las características morfológicas de los insectos vectores
#de la enfermedad del Chagas.

import csv
import re
import json

#Clase creada para el manejo de archivos
class ReadWrite_Files:
	def write_in_json(path,json_file):
		with open(path, 'w') as outfile:
			archivo = json.dump(json_file,outfile)
	def read_csv(path):
		characteristicsArray = []
		with open(path, newline='') as File:
			reader = csv.reader(File)
			for row in reader:
				characteristicsArray.append(row)
		return characteristicsArray
class Get_Descriptions: 

	#Se obtienen las características seleccionadas bajo ciertos criterios
	def get_characteristics():
		characteristicsArray = ReadWrite_Files.read_csv('Clasified_characteristics.csv')
		return characteristicsArray

	#Se obtienen las descripciones de cada característica de cada insecto
	def get_descriptions():
		descriptionsArray = []
		descriptionsFile = open('descriptions_files/insect_descriptions.txt','r')
		descriptionsText = descriptionsFile.read()
		splitDescriptions = descriptionsText.split('\n')
		for i in range(len(splitDescriptions)):
			descriptionsArray.append(splitDescriptions[i].split('@'))
		return descriptionsArray

	#Se almacena la información de cada insecto en un archivo .json
	def get_json_characteristics():
		characteristicsArray = Get_Descriptions.get_characteristics()
		descriptionsArray = Get_Descriptions.get_descriptions()
		insects={}
		characteristics = {}
		textoAux =''
		for i in range(131):
			description = descriptionsArray[i][1]
			for j in range(len(characteristicsArray)):
				coincidences = re.findall(r'('+characteristicsArray[j][0]
					+r'\s[\sa-zA-Z,;\(\)\-0-9\[\]:\+\?]*\.?\s)',description)
				if len(coincidences) != 0:
					characteristics[characteristicsArray[j][0]] = coincidences[0].replace(characteristicsArray[j][0],'')
					insects[''+descriptionsArray[i][0]] = characteristics
			characteristics = {}
		input = {"Especies":insects}
		Get_Descriptions.get_characteristics_files(characteristicsArray,insects)
		path = 'json_insects_data.json'
		ReadWrite_Files.write_in_json(path,input)
		return input

	#Se agrupan las características dependiendo de su tipo, de cada insecto en un archivo de texto
	def get_characteristics_files(characteristicsArray,insects):
		for i in range(len(characteristicsArray)):
			auxFile = open('characteristics_files/'+characteristicsArray[i][0]+'.txt','w')
			for j in insects:
				try:
					auxFile.write(j+'@'+insects[j][characteristicsArray[i][0]].replace(characteristicsArray[i][0]+' ','')+'\n')
				except KeyError: 
					print('', end=" ")
#Clase principal
def main():
	#Tercera fase
	Get_Descriptions.get_json_characteristics()

	
if __name__ == "__main__":
    main()