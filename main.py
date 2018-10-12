import fitz

insectsList = []
pageAux = 121


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])


class Insect:
    def __init__(self, name, initialPage, finalPage, description):
        self.name = name
        self.initialPage = initialPage
        self.finalPage = finalPage
        self.description = description

    def __init__(self, name, initialPage):
        self.name = name
        self.initialPage = initialPage


insectsIndex = open('insectosDesordenado.txt','r')
indexContent = insectsIndex.read()
indexLine = indexContent.split('\n')

for i in range(len(indexLine)):
    line = indexLine[i]
    name = line[line.index(':'):] + ' ' + line[:line.index(',')]
    name = name.replace(':','')
    initialPage = line[line.index(','):line.index(':')]
    initialPage = initialPage.replace(', ','')
    aux = Insect(name, int(initialPage))
    insectsList.append(aux)

insectsList.sort(key=lambda x: x.initialPage)

for m in range(len(insectsList)):
    if insectsList[m].initialPage == 462:
        insectsList[m].finalPage = 464
    else:
        insectsList[m].finalPage = insectsList[m + 1].initialPage

pdfText = fitz.open('LibroTriatominae.pdf')

for n in range(len(insectsList)):
    pagesContent = ''
    description = ''
    for k in range(insectsList[n].initialPage,insectsList[n].finalPage+1):
        singlePageContent = pdfText.loadPage(k-pageAux)
        pagesContent += singlePageContent.getText('text')
        pagesContent = pagesContent.replace('-\n', '')
        pagesContent = pagesContent.replace('  ', ' ')
        pagesContent = pagesContent.replace('\'', '')
        pagesContent = pagesContent.replace('\"', '')
        pagesContent = pagesContent.replace('MARTINFZ', 'MARTINEZ')
        pagesContent = pagesContent.replace('CARCA VALLO', 'CARCAVALLO')
        pagesContent = pagesContent.replace('Be/minus', 'Belminus')
        pagesContent = pagesContent.replace('ST AL', 'STAL')
        pagesContent = pagesContent.replace('mazzattii', 'mazzottii')
        pagesContent = pagesContent.replace('jlavida', 'flavida')
        pagesContent = pagesContent.replace('eratyrusif ormis', 'eratyrusiformis')
        pagesContent = pagesContent.replace('TRIA TO MINI', 'TRIATOMINI')
        pagesContent = pagesContent.replace('stgments', 'segments')
        pagesContent = pagesContent.replace('seg ments', 'segments')
        pagesContent = pagesContent.replace('tu bercles', 'tubercles')
        pagesContent = pagesContent.replace('denti cles.', 'denticles.')
        pagesContent = pagesContent.replace('trapezoi dal', 'trapezoidal')
        pagesContent = pagesContent.replace('un der', 'under')
        pagesContent = pagesContent.replace('an tenniferous', 'antenniferous')
        pagesContent = pagesContent.replace('sub median', 'submedian')
        pagesContent = pagesContent.replace('St!l', 'Stal')
        pagesContent = pagesContent.replace('!', 'l')
        pagesContent = pagesContent.replace('antenna)', 'antennal')
        pagesContent = pagesContent.replace('antenna]', 'antennal')
        pagesContent = pagesContent.replace('Urostemites', 'Urosternites')
        pagesContent = pagesContent.replace('Antennifrous', 'Antenniferous')
        pagesContent = pagesContent.replace('Cori um', 'Corium')
    pagesContent = remove_non_ascii(pagesContent)
    if insectsList[n].name == 'Triatoma barberi' or \
            insectsList[n].name == 'Triatoma mexicana' or \
            insectsList[n].name == 'ERATYRUS STAL' or \
            insectsList[n].name == 'Panstrongylus rufotuberculatus' or \
            insectsList[n].name == 'MICROTRIATOMA PROSEN AND MARTINEZ':
        description = pagesContent[
                      pagesContent.index(insectsList[n].name):pagesContent.index('\n' + insectsList[n + 1].name)]
    elif insectsList[n].name == 'Alberprosenia goyovargasi':
        description = pagesContent[
                      pagesContent.index('\n'+insectsList[n].name):pagesContent.index('\nKEYS IN SPANISH')]
    else:
        description = pagesContent[pagesContent.index('\n'+insectsList[n].name):pagesContent.index('\n'+insectsList[n+1].name)]

    print(description,'\n')