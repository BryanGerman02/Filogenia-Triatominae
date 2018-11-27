import fitz
import json
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]




pdf = fitz.open("C:\\Users\\bryan\\Documents\\Triatominae-Proyecto\\LibroTriatominae.pdf")
archivo = open('infoFromIndex.txt','r')
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
insectos = []
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
	insectos.append(nombre.replace(' ','')+apellido.replace(' ',''))
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
	contenidoEspecifico = contenidoEspecifico.replace('antenna)','antennal')
	contenidoEspecifico = contenidoEspecifico.replace('antenna]','antennal')
	contenidoEspecifico = contenidoEspecifico.replace('Urostemites','Urosternites')
	contenidoEspecifico = contenidoEspecifico.replace('Antennifrous','Antenniferous')
	contenidoEspecifico = contenidoEspecifico.replace('Cori um','Corium')
	#Cori um
	#Antennifrous 
	#Urostemites
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
	contenidoEspecifico = re.sub(r'(\(figs[\.\w\s\d,;\-]*\))','',contenidoEspecifico)
	contenidoEspecifico = re.sub(r'(\(fig[\.\w\s\d,;\-]*\))','',contenidoEspecifico)
	contenidoEspecifico = re.sub(r'(\(as in [\.\w\s\d,;]*\))','',contenidoEspecifico)
	contenidoEspecifico = re.sub(r'(\(see [\.\w\s\d,;]*\))','',contenidoEspecifico)
	#(see fig.6G)
	#(\(as in fig[\.\w\s\d,;]*\))
	contenidoEspecifico = contenidoEspecifico.replace('  ',' ')
	contenidoEspecifico = contenidoEspecifico.replace('\n','@')
	contenidoEspecifico = re.sub(r'(\.@)','.\n',contenidoEspecifico)
	contenidoEspecifico = re.sub(r'(\.\s@)','.\n',contenidoEspecifico)
	contenidoEspecifico = contenidoEspecifico.replace('@','')
	contenidoEspecifico = contenidoEspecifico.replace('fig. ','fig')
	contenidoEspecifico = re.sub(r'(mm\.)','',contenidoEspecifico)
	contenidoEspecifico = re.sub(r'(\w+ly)','',contenidoEspecifico)
	contenidoEspecifico = contenidoEspecifico.replace('T.','T')
	'''contenidoEspecifico = contenidoEspecifico.replace('.',' . ')
	contenidoEspecifico = contenidoEspecifico.replace(',',' , ')
	contenidoEspecifico = contenidoEspecifico.replace(';',' ; ')
	contenidoEspecifico = contenidoEspecifico.replace(')',' ) ')
	contenidoEspecifico = contenidoEspecifico.replace('(',' ( ')
	contenidoEspecifico = contenidoEspecifico.replace(':',' : ')
	contenidoEspecifico = contenidoEspecifico.replace(',',' , ')'''
	contenidoEspecifico = " ".join( contenidoEspecifico.split() )
	wordList = contenidoEspecifico.split()
	wordList = removeStopwords(wordList,stopwords)
	contenidoEspecifico = ''
	for i in wordList:
		contenidoEspecifico += i + ' '
	archivo = open('C:\\Users\\bryan\\Documents\\Github\\Filogenia-Triatominae\\ArchivoCompleto\\descriptions.txt','a',encoding='utf-8')
	archivo.write(nombre+' '+apellido+'@'+contenidoEspecifico+'\n')
	contenidoSeparado = contenidoEspecifico.split('\n')
	partesDelContenido = {}
	referencia = ''
	referencia = contenidoSeparado[0]
	informacionPartes = ''
	for i in range(1,len(contenidoSeparado)):
		informacionPartes += ' '+contenidoSeparado[i]
	informacionPartes = informacionPartes[1:len(informacionPartes)-1]
	informacionPartes = informacionPartes.replace('figs.','figs')
	informacionPartes = informacionPartes.replace('viz.','viz')
	#proporcion de 3 -> (\d:\d\.\d*:\d*\.\d*)
	#proporcion de 3(rangos) -> (\d:\d.\d*\-\d\.\d:\d\.\d-\d\.\d:\d\.\d\-\d\.\d)
	#proporcion de 2 -> (\d:\d.\d*)
	#proporcion de 2 (rangos) ->(\d:\d.\d*\-\d\.\d)
	#proporcion de 1 -> (\d:\d\.\d)
	textoAux = informacionPartes
	partes = {}
	auxPartes = ''
	nombreParte = ''
	descripcion = ''
	for i in range(len(partesInsectos)):
		#print(nombreInsecto)
		#print(partesInsectos[i])
		#auxPartes = re.findall(r'('+partesInsectos[i]+r'[:\s][\sa-zA-Z,\-;]*\.)',informacionPartes)
		decimales = []
		decimales = re.findall(r'\d\.\d',textoAux)
		for k in range(len(decimales)):
			textoAux = textoAux.replace(decimales[k],decimales[k].replace('.',','))
		auxPartes = re.findall(r'('+partesInsectos[i]+r'\s[\sa-zA-Z,;\(\)\-0-9\[\]:\+\?]*\.?)',textoAux)
		#print(auxPartes)
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
	partesDelContenido['Informacion no procesada']=textoAux
	jsonFinal[nombre+" "+apellido] = {"pagina":""+str(paginaInsecto)+""  , "informacion":partesDelContenido}
	contenidoEspecifico = ''	
formatoJson = str(jsonFinal).replace("\'","\"").replace('\\x','/x').replace('- ','')
formatoJson = formatoJson.replace('\\n',' ')
formatoJson = re.sub(r'(/xad\s?)','',formatoJson)
print(str(insectos).replace('\'','').replace('[','{').replace(']','}'))
input = {"Especies":jsonFinal}
        

#print(type(jsonObjectInfo))
#print(jsonObjectInfo)
'''distanceMatrix = str(jsonObjectInfo["Especies"][1]["informacion"])
distanceMatrix = distanceMatrix[distanceMatrix.index('DISTRIBUTION'):]
distanceMatrix = distanceMatrix[distanceMatrix.index('Triatoma Laporte'):]'''
with open('data.json', 'w') as outfile:
    archivo = json.dump(input,outfile)
#print(str(jsonObjectInfo["Especies"][1]["pagina"]))
#print(str(jsonObjectInfo["Especies"][1]["nombreInsecto"]))
#print(distanceMatrix)
#print(distanceMatrix)