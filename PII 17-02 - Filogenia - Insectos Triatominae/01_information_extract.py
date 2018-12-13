import fitz
import re


class Insect:
	page = ''
	name = ''
	last_name = ''
	def __init__(self, page,name,last_name):
		self.page = page
		self.name = name
		self.last_name = last_name
	
class Information_extract: 

	def extract_index():
		file = open('insects_index.txt','r')
		index_content = file.read()
		split_index = index_content.split('\n')
		split_index = sorted(split_index)
		return split_index

	def get_Content(initial_page, final_page):
		specific_content = ''
		pdf = fitz.open("LibroTriatominae.pdf")
		for i in range(initial_page-120-1, final_page-120):
			page = pdf.loadPage(i)
			specific_content += page.getText("text")
		return specific_content

	def edit_wrong_names(insect_description):
		insect_description = insect_description.replace('-\n','')
		insect_description = insect_description.replace('  ',' ')
		insect_description = insect_description.replace('\'','')
		insect_description = insect_description.replace('\"','')
		insect_description = insect_description.replace('MARTINFZ','MARTINEZ')
		insect_description = insect_description.replace('CARCA VALLO','CARCAVALLO')
		insect_description = insect_description.replace('Be/minus','Belminus')
		insect_description = insect_description.replace('ST AL','STAL')
		insect_description = insect_description.replace('mazzattii','mazzottii')
		insect_description = insect_description.replace('jlavida','flavida')
		insect_description = insect_description.replace('eratyrusif ormis','eratyrusiformis')
		insect_description = insect_description.replace('TRIA TO MINI','TRIATOMINI')
		insect_description = insect_description.replace('stgments','segments')
		insect_description = insect_description.replace('seg ments','segments')
		insect_description = insect_description.replace('tu bercles','tubercles')
		insect_description = insect_description.replace('denti cles.','denticles.')
		insect_description = insect_description.replace('trapezoi dal','trapezoidal')
		insect_description = insect_description.replace('un der','under')
		insect_description = insect_description.replace('an tenniferous','antenniferous')
		insect_description = insect_description.replace('sub median','submedian')
		insect_description = insect_description.replace('St!l','Stal')
		insect_description = insect_description.replace('MATERIAL EXAMINED','TYPE')
		insect_description = insect_description.replace('!','l')
		insect_description = insect_description.replace('fig. ','fig.')
		insect_description = insect_description.replace('antenna)','antennal')
		insect_description = insect_description.replace('antenna]','antennal')
		insect_description = insect_description.replace('Urostemites','Urosternites')
		insect_description = insect_description.replace('Antennifrous','Antenniferous')
		insect_description = insect_description.replace('Cori um','Corium')
		return insect_description

	def extract_content_insect():
		index_insects = Information_extract.extract_index()
		for index_item in range(len(index_insects)):
			split_index_insects = index_insects[index_item].split(':')
			split_insect_description_insects = split_index_insects[1].split(',')
			actual_insect = Insect(split_index_insects[0],split_insect_description_insects[0],split_insect_description_insects[1])
			if index_insects[index_item] != index_insects[-1]:
				split_next_index_insects = index_insects[index_item+1].split(':')
				next_insect = Insect(split_next_index_insects[0],'','')
			else:
				next_insect = Insect('464','','')
			insect_description = Information_extract.get_Content(int(actual_insect.page),int(next_insect.page))
			insect_description = Information_extract.edit_wrong_names(insect_description)
			insect_description = Information_extract.delete_repeated_phrases(actual_insect.last_name,insect_description)
			insect_description = Information_extract.delimit_content(insect_description,actual_insect.page,actual_insect.name,actual_insect.last_name)
			insect_description = Information_extract.delete_fig_references(insect_description)
			insect_description = Information_extract.separe_paraghraps(insect_description)
			insect_description = Information_extract.fix_decimals(insect_description)
			
			#GUARDAR EN ARCHIVOS DIFERENTES PARA LA EXTRACCION DE CARACTERISTICAS
			path = 'descriptions_separated_files\\'+str(index_item)+'.txt'
			Write_Files.save_insects_different_txtfiles(path,insect_description)
			#PASA DE PYTHON A R --> Archivo R-DataSet.R

			#GUARDAR EN UN SOLO ARCHIVO TODAS LAS DESCRIPCIONES
			path = 'descriptions_files\\insect_descriptions.txt'
			Write_Files.save_insect_descriptions_in_txtfile(path,insect_description,actual_insect.name,actual_insect.last_name)
			#PASA A LA SEPARACION DE ARCHIVOS DE CARACTERISTICAS
	
	def delete_repeated_phrases(last_name,insect_description):
		if(last_name == 'Laporte'):
			insect_description = insect_description.replace('Triatoma Laporte, 1832. ','')
		if(last_name == 'hirsuta Barber'):
			insect_description = insect_description.replace('Paratriatoma hirsuta Barber. DISTRIBUTION:','')
		if(last_name == 'goyovargasi'):
			insect_description = insect_description.replace('Alberprosenia goyovargasi Martinez and Carcavallo, 1977','')
		if(last_name == 'rubrofasciata'):
			insect_description = insect_description.replace('Triatoma rubrofasciata, which is superficially similar to rubida, but the former species is conspicuously granulose on the head and pronotum, and rubida is not.','')
		if(last_name == 'costalis'):
			insect_description = insect_description.replace('Linshcosteus costalis. OBSERVATIONS: ','')
		if(last_name == 'maximus'):
			insect_description = insect_description.replace('Dipetalogaster maximus possesses other characters','')
		if(last_name == 'Stal'):
			insect_description = insect_description.replace('Rhodnius Stal, 1859. Other genus included: Psammolestes Bergroth, 1911. ','')
		if(last_name == 'pilosa'):
			insect_description = insect_description.replace('Cavernicola pilosa Barber, 1937. ','')
		if(last_name == 'scabrosa'):
			insect_description = insect_description.replace('Bolbodera scabrosa Valdes; type species of','')
		if(last_name == 'Valdes'):
			insect_description = insect_description.replace('BIOLOGY:','TYPE:')
		return insect_description

	def delimit_content(insect_description,page,name,last_name):
		try: 
			insect_description = insect_description[insect_description.index(name +" "+ last_name):]
		except ValueError:
			print('Insect not found'+name+' '+last_name,insect_description)
		try:
			insect_description = insect_description[:insect_description.index('TYPE')]
			return insect_description
		except ValueError:
			print('Delimit not found')	

	def delete_fig_references(insect_description):
		insect_description = str(insect_description.encode('utf-8'))
		insect_description = insect_description[1:].replace('\\','/').replace('/xc2/xad ','').replace('/xc2/xad','').replace('/xc2/xb7','').replace('/xef/xbf/xbd','').replace('/xc2/xb1','').replace('/','\\').replace('\'','').replace('\\n','\n').strip(' ')
		insect_description = re.sub(r'(\(figs[\.\w\s\d,;\-]*\))','',insect_description)
		insect_description = re.sub(r'(\(fig[\.\w\s\d,;\-]*\))','',insect_description)
		insect_description = re.sub(r'(\(as in [\.\w\s\d,;]*\))','',insect_description)
		insect_description = re.sub(r'(\(see [\.\w\s\d,;]*\))','',insect_description)
		return insect_description

	def separe_paraghraps(insect_description):
		insect_description = insect_description.replace('  ',' ')
		insect_description = insect_description.replace('\n','@')
		insect_description = re.sub(r'(\.@)','.\n',insect_description)
		insect_description = re.sub(r'(\.\s@)','.\n',insect_description)
		insect_description = insect_description.replace('@','')
		insect_description = insect_description.replace('fig. ','fig')
		insect_description = re.sub(r'(mm\.)','',insect_description)
		insect_description = insect_description.replace('T.','T')
		insect_description = " ".join( insect_description.split() )	
		return insect_description
	
	def fix_decimals(insect_description):
		insect_description = re.sub(r':\s',':',insect_description)
		decimals = []
		decimals = re.findall(r'\d\.\s\d',insect_description)
		for k in range(len(decimals)):
			insect_description = insect_description.replace(decimals[k],decimals[k].replace('. ','.'))
		decimals = re.findall(r'\d\.\d',insect_description)
		for k in range(len(decimals)):
			insect_description = insect_description.replace(decimals[k],decimals[k].replace('.',','))
		return insect_description
	
	
			
class Write_Files:
	def save_insect_descriptions_in_txtfile(file_path,text,insect_name,insect_last_name):
		file = open(file_path,'a',encoding = 'utf-8')
		file.write(insect_name+' '+insect_last_name+'@'+text+'\n')
		file.close()
	def save_insects_different_txtfiles(file_path,text):
		file = open(file_path,'w',encoding = 'utf-8')
		file.write(text)
		file.close()



			

def main():
	#Primera fase
	Information_extract.extract_content_insect()
	
if __name__ == "__main__":
    main()