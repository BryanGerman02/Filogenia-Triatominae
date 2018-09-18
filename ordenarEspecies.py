import fitz
import json
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
pdf = fitz.open("C:\\Users\\bryan\\Documents\\Triatominae-Proyecto\\LibroTriatominae.pdf")
archivo = open('insectosDesordenado.txt','r')
contenido = archivo.read()
separar = contenido.split('\n')
diccionariInsectos = {}
final = ''
arregloDesordenado = []
arregloOrdenado = []
jsonFinal = {
}
for i in range(len(separar)):
	if ',' in separar[i]:
		linea = str(separar[i])
		linea = linea[linea.index(','):]+ ';'+linea[:linea.index(',')]
		linea = linea.replace(',','')
		linea  = linea.strip()
		arregloDesordenado.append(linea)
		
	else:
		arregloDesordenado.append(str(separar[i]))
arregloOrdenado = sorted(arregloDesordenado)
#for i in range(len(arregloOrdenado)):
#	print('i: '+str(i) + ' insecto: ' +arregloOrdenado[i] )
contenidoEspecifico = ''
insecto = ''
insectoSiguiente = ''
paginaInsecto = 0
paginaInsectoSiguiente = 0
nombreInsecto = ''
nombreInsectoSiguiente = ''
informacionInsecto = ''
contenidoSeparado = ''
jsonFinal={}
archivoPartesInsectos =open('partesTriatominae.csv','r')
print(archivoPartesInsectos)
textoPartesInsectos = archivoPartesInsectos.read()
partesInsectos = textoPartesInsectos.split('\n')
archivoPrueba = open('archivoPrueba.txt','a')
for x in range(len(arregloOrdenado)):
	insecto = arregloOrdenado[x].split(':')
	paginaInsecto = int(insecto[0])
	nombreInsecto = insecto[1]
	separarNombreInsecto = nombreInsecto.split(';')
	nombre = separarNombreInsecto[0]
	apellido = separarNombreInsecto[1]
	if(x == len(arregloOrdenado)-1):
		paginaInsectoSiguiente = 464 
	else:
		insectoSiguiente = arregloOrdenado[x+1].split(':')
		paginaInsectoSiguiente = int(insectoSiguiente[0])
		nombreInsectoSiguiente = insectoSiguiente[1]
	if(nombre == 'Tnatoma'):
		nombre = 'Triatoma'
	if(nombre == 'Cavemnicola'):
		nombre = 'Cavernicola'
	for i in range(paginaInsecto-120-1, paginaInsectoSiguiente-120):
		page = pdf.loadPage(i)
		contenidoEspecifico += page.getText("text")
	aux = ''
	contenidoEspecifico = contenidoEspecifico.replace('-\n','')
	contenidoEspecifico = contenidoEspecifico.replace('  ',' ')
	contenidoEspecifico = contenidoEspecifico.replace('\'','')
	contenidoEspecifico = contenidoEspecifico.replace('\"','')
	contenidoEspecifico = contenidoEspecifico.replace('MARTINFZ','MARTINEZ')
	contenidoEspecifico = contenidoEspecifico.replace('CARCA VALLO','CARCAVALLO')
	contenidoEspecifico = contenidoEspecifico.replace('Be/minus','Belminus')
	contenidoEspecifico = contenidoEspecifico.replace('ST AL','STAL')
	contenidoEspecifico = contenidoEspecifico.replace('mazzattii','mazzottii')
	contenidoEspecifico = contenidoEspecifico.replace('jlavida','flavida')
	contenidoEspecifico = contenidoEspecifico.replace('eratyrusif ormis','eratyrusiformis')
	contenidoEspecifico = contenidoEspecifico.replace('TRIA TO MINI','TRIATOMINI')
	contenidoEspecifico = contenidoEspecifico.replace('stgments','segments')
	contenidoEspecifico = contenidoEspecifico.replace('seg ments','segments')
	contenidoEspecifico = contenidoEspecifico.replace('tu bercles','tubercles')
	contenidoEspecifico = contenidoEspecifico.replace('denti cles.','denticles.')
	contenidoEspecifico = contenidoEspecifico.replace('trapezoi dal','trapezoidal')
	contenidoEspecifico = contenidoEspecifico.replace('un der','under')
	contenidoEspecifico = contenidoEspecifico.replace('an tenniferous','antenniferous')
	contenidoEspecifico = contenidoEspecifico.replace('sub median','submedian')
	contenidoEspecifico = contenidoEspecifico.replace('St!l','Stal')
	contenidoEspecifico = contenidoEspecifico.replace('MATERIAL EXAMINED','TYPE')
	contenidoEspecifico = contenidoEspecifico.replace('!','l')
	contenidoEspecifico = contenidoEspecifico.replace('fig. ','fig.')
	#MARTINFZ
	#CARCA VALLO
	#Be/minus
	#ST AL
	#mazzattii mazzottii
	#jlavida
	#eratyrusif ormis
	#TRIA  TO  MINI
	if(apellido == 'Laporte'):
		contenidoEspecifico = contenidoEspecifico.replace('Triatoma Laporte, 1832. ','')
	if(apellido == 'hirsuta Barber'):
		contenidoEspecifico = contenidoEspecifico.replace('Paratriatoma hirsuta Barber. DISTRIBUTION:','')
	if(apellido == 'goyovargasi'):
		contenidoEspecifico = contenidoEspecifico.replace('Alberprosenia goyovargasi Martinez and Carcavallo, 1977','')
	if(apellido == 'rubrofasciata'):
		contenidoEspecifico = contenidoEspecifico.replace('Triatoma rubrofasciata, which is superficially similar to rubida, but the former species is conspicuously granulose on the head and pronotum, and rubida is not.','')
	if(apellido == 'costalis'):
		contenidoEspecifico = contenidoEspecifico.replace('Linshcosteus costalis. OBSERVATIONS: ','')
	if(apellido == 'maximus'):
		contenidoEspecifico = contenidoEspecifico.replace('Dipetalogaster maximus possesses other characters','')
	if(apellido == 'Stal'):
		contenidoEspecifico = contenidoEspecifico.replace('Rhodnius Stal, 1859. Other genus included: Psammolestes Bergroth, 1911. ','')
	if(apellido == 'pilosa'):
		contenidoEspecifico = contenidoEspecifico.replace('Cavernicola pilosa Barber, 1937. ','')
	if(apellido == 'scabrosa'):
		contenidoEspecifico = contenidoEspecifico.replace('Bolbodera scabrosa Valdes; type species of','')
	if(apellido == 'Valdes'):
		contenidoEspecifico = contenidoEspecifico.replace('BIOLOGY:','TYPE:')
	try: 
		contenidoEspecifico = contenidoEspecifico[contenidoEspecifico.index(nombre +" "+ apellido):]
	except ValueError:
		print('\n******\nEn la pagina: '+str(paginaInsecto)+', insecto: '+nombre +' '+apellido+'\nNo se encuentra nombre en: \n'+contenidoEspecifico)
	try:
		contenidoEspecifico = contenidoEspecifico[:contenidoEspecifico.index('TYPE')]
	except ValueError:
		print('\n******\nEn la pagina: '+str(paginaInsecto)+', insecto: '+nombre +' '+apellido+'\nNo se encuentra TYPE en: \n'+contenidoEspecifico)	
	contenidoEspecifico = str(contenidoEspecifico.encode('utf-8'))
	contenidoEspecifico = contenidoEspecifico[1:].replace('\\','/').replace('/xc2/xad ','').replace('/xc2/xad','').replace('/xc2/xb7','').replace('/xef/xbf/xbd','').replace('/xc2/xb1','').replace('/','\\').replace('\'','').replace('\\n','\n').strip(' ')
	contenidoEspecifico = re.sub(r'(\(figs.[\w\s\d,]*\))','',contenidoEspecifico)
	contenidoEspecifico = re.sub(r'(\(fig.[\w\s\d,]*\))','',contenidoEspecifico)
	contenidoEspecifico = contenidoEspecifico.replace('  ',' ')
	contenidoEspecifico = contenidoEspecifico.replace('\n','@')
	contenidoEspecifico = re.sub(r'(\.@)','.\n',contenidoEspecifico)
	contenidoEspecifico = re.sub(r'(\.\s@)','.\n',contenidoEspecifico)
	contenidoEspecifico = contenidoEspecifico.replace('@','')
	contenidoEspecifico = contenidoEspecifico.replace('fig. ','fig.')
	contenidoEspecifico = contenidoEspecifico.replace('mm. ','mm.')
	contenidoEspecifico = contenidoEspecifico.replace('T.','T.')
	contenidoSeparado = contenidoEspecifico.split('\n')
	partesDelContenido = {}
	referencia = ''
	referencia = contenidoSeparado[0]
	informacionPartes = ''
	for i in range(1,len(contenidoSeparado)):
		informacionPartes += ' '+contenidoSeparado[i]
	informacionPartes = informacionPartes[1:len(informacionPartes)-1]
	textoAux = informacionPartes
	partes = {}
	auxPartes = ''
	nombreParte = ''
	descripcion = ''
	for i in range(len(partesInsectos)):
		print(nombreInsecto)
		print(partesInsectos[i])
		#auxPartes = re.findall(r'('+partesInsectos[i]+r'[:\s][\sa-zA-Z,\-;]*\.)',informacionPartes)
		auxPartes = re.findall(r'('+partesInsectos[i]+r'\s[\sa-zA-Z,;\(\)\-0-9\[\]:]*\.?\s?)',textoAux)
		print(auxPartes)
		if(len(auxPartes) != 0):
			if(len(auxPartes) > 1):
				tamanio = len(auxPartes)
				segmentos = ''
				j=0
				for j in range(tamanio):
					segmentos += ' '+ auxPartes[j]
					textoAux = textoAux.replace(auxPartes[j],'')
				segmentos = segmentos.replace(''+partesInsectos[i],'') 
				partes[''+partesInsectos[i]] = segmentos
			else:
				partes[''+partesInsectos[i]] = auxPartes[0].replace(''+partesInsectos[i],'')
				textoAux = textoAux.replace(auxPartes[0],'')
		auxPartes=[]
	#print('\n*********************\ninsecto: '+nombreInsecto + "\n arreglo: \n"+str(separarPartes)+"\n***********************\n")		 
	#for i in range(len(arregloPartes)):
	#	arregloPartes[i] = arregloPartes[i][2:]
	#archivoPrueba.write('\n*********************\ninsecto: '+nombreInsecto + "\n arreglo: \n"+str(arregloPartes)+"\n***********************\n")
	partesDelContenido['referencia'] = referencia
	partesDelContenido['partes'] = partes
	jsonFinal[nombre+" "+apellido] = {"pagina":""+str(paginaInsecto)+""  , "informacion":partesDelContenido}
	contenidoEspecifico = ''	
formatoJson = str(jsonFinal).replace("\'","\"").replace('\\x','/x').replace('- ','')
formatoJson = formatoJson.replace('\\n',' ')
formatoJson = re.sub(r'(/xad\s?)','',formatoJson)

input = {"Especies":jsonFinal}
        

#print(type(jsonObjectInfo))
#print(jsonObjectInfo)
'''aux = str(jsonObjectInfo["Especies"][1]["informacion"])
aux = aux[aux.index('DISTRIBUTION'):]
aux = aux[aux.index('Triatoma Laporte'):]'''
with open('data.json', 'w') as outfile:
    archivo = json.dump(input,outfile)
#print(str(jsonObjectInfo["Especies"][1]["pagina"]))
#print(str(jsonObjectInfo["Especies"][1]["nombreInsecto"]))
#print(aux)
#print(aux)