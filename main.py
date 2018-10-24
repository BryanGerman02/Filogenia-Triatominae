import fitz
import re

insectsList = []
pageAux = 121


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


insectsIndex = open('infoFromIndex.txt','r')
indexContent = insectsIndex.read()
indexLine = indexContent.split('\n')

i = 0

for i in range(len(indexLine)):
    line = indexLine[i]
    name = line[line.index(':'):] + ' ' + line[:line.index(',')]
    name = name.replace(':','')
    initialPage = line[line.index(','):line.index(':')]
    initialPage = initialPage.replace(', ','')
    aux = Insect(name, int(initialPage))
    insectsList.append(aux)

insectsList.sort(key=lambda x: x.initialPage)

m = 0

for m in range(len(insectsList)):
    if insectsList[m].initialPage == 462:
        insectsList[m].finalPage = 464
    else:
        insectsList[m].finalPage = insectsList[m + 1].initialPage

pdfText = fitz.open('LibroTriatominae.pdf')

n = 0

for n in range(len(insectsList)):
    pagesContent = ''
    description = ''

    k = 0

    for k in range(insectsList[n].initialPage,insectsList[n].finalPage+1):
        singlePageContent = pdfText.loadPage(k-pageAux)
        pagesContent += singlePageContent.getText('text')
    pagesContent = remove_non_ascii(pagesContent)
    pagesContent = pagesContent.replace('-\n', '')
    pagesContent = pagesContent.replace('  ', ' ')
    pagesContent = pagesContent.replace('\'', '')
    pagesContent = pagesContent.replace('\"', '')
    pagesContent = pagesContent.replace('MARTINFZ', 'MARTINEZ')
    pagesContent = pagesContent.replace('CARCA VALLO', 'CARCAVALLO')
    pagesContent = pagesContent.replace('CARCAV ALLO', 'CARCAVALLO')
    pagesContent = pagesContent.replace('Be/minus', 'Belminus')
    pagesContent = pagesContent.replace('ST AL', 'STAL')
    pagesContent = pagesContent.replace('mazzattii', 'mazzottii')
    pagesContent = pagesContent.replace('jlavida', 'flavida')
    pagesContent = pagesContent.replace('eratyrusif ormis', 'eratyrusiformis')
    pagesContent = pagesContent.replace('TRIA TO MINI', 'TRIATOMINI')
    pagesContent = pagesContent.replace('CAVERN/COLA', 'CAVERNICOLA')
    pagesContent = pagesContent.replace('St!l', 'Stal')
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

    description = re.sub(r'(\(figs[\.\w\s\d,;\-]*\))', '', description)
    description = re.sub(r'(\(fig[\.\w\s\d,;\-]*\))', '', description)
    description = re.sub(r'(\(as in [\.\w\s\d,;]*\))', '', description)
    description = re.sub(r'(\(see [\.\w\s\d,;]*\))', '', description)
    description = description.replace('  ', ' ')
    description = description.replace('\n', '@')
    description = re.sub(r'(\.@)', '.\n', description)
    description = re.sub(r'(\.\s@)', '.\n', description)
    description = description.replace('@', '')
    description = description.replace('fig. ', 'fig')
    description = re.sub(r'(mm\.)', 'mm', description)
    description = description.replace('T.', 'T')
    description = description.replace('stgments', 'segments')
    description = description.replace('seg ments', 'segments')
    description = description.replace('tu bercles', 'tubercles')
    description = description.replace('denti cles.', 'denticles.')
    description = description.replace('trapezoi dal', 'trapezoidal')
    description = description.replace('un der', 'under')
    description = description.replace('an tenniferous', 'antenniferous')
    description = description.replace('sub ', 'sub')
    description = description.replace('!', 'l')
    description = description.replace('antenna)', 'antennal')
    description = description.replace('antenna]', 'antennal')
    description = description.replace('Urostemites', 'Urosternites')
    description = description.replace('Antennifrous', 'Antenniferous')
    description = description.replace('Cori um', 'Corium')
    description = description.replace('abdomi nal', 'abdominal')
    description = description.replace('Aba los', 'Abalos')
    description = description.replace('aex', 'apex')
    description = description.replace('Af rica', 'Africa')
    description = description.replace('comer', 'corner')
    description = description.replace('hav ing', 'having')
    description = description.replace('Aus tralia', 'Australia')
    description = description.replace('pat tern', 'pattern')
    description = description.replace('re stricted', 'restricted')
    description = description.replace('re duced', 'reduced')
    description = description.replace('re mote', 'remote')
    description = description.replace('re gion', 'region')
    description = description.replace('cub re', 'cubre')
    description = description.replace('re fer', 'refer')
    description = description.replace('re mainder', 'remainder')
    description = description.replace('re ported', 'reported')
    description = description.replace('Re maining', 'Remaining')
    description = description.replace('re lated', 'related')
    description = description.replace('di vided', 'divided')
    description = description.replace('indi cate', 'indicate')
    description = description.replace('medi ally', 'medially')
    description = description.replace('di ameter', 'diameter')
    description = description.replace('ddi tional', 'dditional')
    description = description.replace('di rected', 'directed')
    description = description.replace('interseg mental', 'intersegmental')
    description = description.replace('seg ment', 'segment')
    description = description.replace('con nexival', 'connexival')
    description = description.replace('con siderably', 'considerably')
    description = description.replace('con vex', 'convex')
    description = description.replace('con verging', 'converging')
    description = description.replace('con spicuously', 'conspicuously')
    description = description.replace('con stricted', 'constricted')
    description = description.replace('con colorous', 'concolorous')
    description = description.replace('sym patric', 'sympatric')
    description = description.replace('speci men', 'specimen')
    description = description.replace('den ticle', 'denticle')
    description = description.replace('diffi cult', 'difficult')
    description = description.replace('sim ple', 'simple')
    description = description.replace(' l ', ' 1 ')
    description = description.replace(' lyellow', ' 1 yellow')
    description = description.replace('Ala ry', 'Alary')
    description = description.replace('albi ventris', 'albiventris')
    description = description.replace('V ALOES', 'VALDES')
    description = description.replace('Amaryl lidaceae', 'Amaryllidaceae')
    description = description.replace('ami citiae', 'amicitiae')
    description = description.replace('ex amined', 'examined')
    description = description.replace('mexieana', 'mexicana')
    description = description.replace('anddark', 'and dark')
    description = description.replace('andjaegeri', 'and jaegeri')
    description = description.replace('angu lar', 'angular')
    description = description.replace('in f estans', 'infestans')
    description = description.replace('por tion', 'portion')
    description = description.replace('pro- notum', 'pronotum')
    description = description.replace('lat ter', 'latter')
    description = description.replace('lat eral', 'lateral')
    description = description.replace('gran ulose', 'granulose')
    description = description.replace('cari nate', 'carinate')
    description = description.replace('compo nent', 'component')
    description = description.replace('de scription', 'descrption')
    description = description.replace('pronotum I. 6', 'pronotum 1.6')
    description = description.replace('ab domen', 'abdomen')
    description = description.replace('red dish', 'reddish')
    description = description.replace('Jong', 'long')
    description = description.replace('tri chobothria', 'trichobothria')
    description = description.replace('segments I: 1', 'segments 1:1')
    description = description.replace('pro notum', 'pronotum')
    description = description.replace('flar ing', 'flaring')
    description = description.replace('coarse ly', 'coarsely')
    description = description.replace('fig ures', 'figures')
    description = description.replace('l:', '1:')
    description = description.replace(':l', ':1')
    description = description.replace('-l0', '-10')
    description = description.replace('-l.', '-1.')
    description = description.replace(' ing', 'ing')
    description = description.replace(': l.', ':1.')
    description = description.replace(': l ', ':1')
    description = description.replace('at taining', 'attaining')
    description = description.replace('oste rior', 'osterior')
    description = description.replace('Subme dian', 'Submedian')
    description = description.replace('subconi cal', 'subconical')
    description = description.replace('BIOLOOY', 'BIOLOGY')
    description = description.replace('spec imen', 'specimen')
    description = description.replace('', '')


    insectsList[n].description = description


def stripNonAlphaNum(text):
    import re
    return re.compile(r'\W+', re.UNICODE).split(text)


def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]


def removeAdjectives(wordlist, adjectives):
    return [z for z in wordlist if z not in adjectives]


def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


file1 = open('allDescriptions.txt','w')
file2 = open('wordsFreq.txt','w')
file3 = open('wordsFreqWithoutStopwords.txt','w')
file4 = open('wordsWoAdjectives.txt','w')

Text = ''

m = 0

for m in range(len(insectsList)):
    Text += insectsList[m].description
    Text += '\n\n'

file1.write(Text)


Text = Text.lower()
Text = re.sub(r'\d*', '', Text)
fullwordlist = stripNonAlphaNum(Text)
dictionary = wordListToFreqDict(fullwordlist)
sorteddict = sortFreqDict(dictionary)

file1.write('\n\n\nNúmero de palabras: ')
file1.write(str(len(fullwordlist)))

file2.write('\nEntradas: ')
file2.write(str(len(sorteddict)))
file2.write('\nNúmero de palabras: ')
file2.write(str(len(fullwordlist)))

s = 0

for s in sorteddict:
    file2.write('\n')
    file2.write(str(s))


wordlist = removeStopwords(fullwordlist, stopwords)
dictionary = wordListToFreqDict(wordlist)
sorteddict = sortFreqDict(dictionary)


file3.write('Entradas: ')
file3.write(str(len(sorteddict)))
file3.write('\nNúmero de palabras: ')
file3.write(str(len(wordlist)))

q = 0

for q in sorteddict:
    file3.write('\n')
    file3.write(str(q))


adjectives = open('adjectives.txt','r').read().split()

wordlist = removeAdjectives(fullwordlist, adjectives)
wordlist1 = removeStopwords(wordlist,stopwords)
dictionary = wordListToFreqDict(wordlist1)
sorteddict = sortFreqDict(dictionary)

file4.write('Entradas: ')
file4.write(str(len(sorteddict)))
file4.write('\nNúmero de palabras: ')
file4.write(str(len(wordlist)))

q = 0

for q in sorteddict:
    file4.write('\n')
    file4.write(str(q))

file1.close()
file2.close()
file3.close()
file4.close()