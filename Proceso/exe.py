import sys
sys.modules[__name__].__dict__.clear()
import json
import numpy as np
from sklearn.decomposition import PCA
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
def addList(numberList):
    addResult = 0
    for i in numberList:
        addResult = addResult + i
    return addResult

path = 'Abdomen'
aux = []
sumas = []
distancia = 0
file = open('CharValues/'+path+'.txt','r').read()
print(path,'\n\n')
if file != '':
    content = file.split('\n')
    j=0
    for j in range(len(content)):
        if content[j] != '':
            content[j] = content[j][content[j].index('@'):].replace('@','')
    for i in range(len(content)):
        content[i] = content[i].split()
    for i in range(len(content)):
        lon = []
        suma = 0
        for j in range(len(content)):
            distancia = len(set(content[i]).union(content[j])) - len(set(content[i]).intersection(content[j]))
            lon.append(distancia)
            suma += distancia
        sumas.append(suma)
        aux.append(lon)
    X = aux
    pca = PCA(n_components=2)
    X3d = pca.fit_transform(X)
    xpoints = []
    ypoints = []
    i = 0
    for i in range(0,len(X3d)):
        xpoints.append(float(X3d[i][0]))
        ypoints.append(float(X3d[i][1]))
    x1 = np.array(xpoints)
    x2 = np.array(ypoints)
    '''plt.plot()
    plt.title('Dataset')
    plt.scatter(x1,x2)
    plt.show()
    # create new plot and data
    plt.plot()'''
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
    colors = ['b', 'g', 'r']
    markers = ['o', 'v', 's']
    # k means determine k
    distortions = []
    K = range(1,10)
    derivadas = []
    resultados = []
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
    for t in range(1,len(distortions)-1):
        derivadas.append(distortions[t + 1] + distortions[t - 1] - (2 * distortions[t]))
    #cluster creation
    aux = []
    sumas = []
    distancia = 0
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(file.split('\n'))
    true_k = derivadas.index(max(derivadas)) + 2
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    #print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    allTerms = []
    for i in range(true_k):
        termsCluster = []
        #print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            termsCluster.append(terms[ind])
        allTerms.append(termsCluster)

contenido = file.split('\n')
i = 0 
matrixValues = []
for i in range(len(contenido)):
    description = ''
    name = ''
    maxValue = 0
    if(contenido[i] != ''):
        add = 0
        if contenido[i] != '':
            contenido[i] = re.sub(r'[:;,.]', '', contenido[i])
            name = contenido[i][:contenido[i].index('@')].replace('@', '')
            description = contenido[i][contenido[i].index('@'):].replace('@', '')
        values = []
        for j in range(len(allTerms)):
            for k in range(len(allTerms[j])):
                tupleValue = allTerms[j][k]
                tupleWeigth = allTerms[j].index(allTerms[j][k])
                if(tupleValue in description):
                    add = add + int(tupleWeigth)
            values.append(add)
            add = 0    
            '''splitContent = contenido[i].split()
            values.append(len(set(contenido[i].split()).intersection(allTerms[j])))'''
            #print('\n',allTerms[j],'all terms')
            #print('********',contenido[i], 'contenido')
        #print(values, 'values')
        if(addList(values) == 0):
            maxValue = '?'
        else: 
            maxValue = values.index(max(values))
        matrixValues.append((name,description,maxValue))
print(matrixValues)
fileJson = open("data.json")
dataJson = json.load(fileJson)
fileJson.close()
#print(re.sub(r'[:;,.]', '', dataJson['Especies'][matrixValues[0][0]]['Abdomen']) == matrixValues[0][1])

for especies in dataJson:
    for especie in dataJson[especies]:
        especieName = especie
        for i in range(len(matrixValues)):
            if(especieName in matrixValues[i]):
                print(especieName,matrixValues[i],especieName in matrixValues[i]) 
                break
            else:
                print(especieName,matrixValues[i],especieName in matrixValues[i]) 
        '''for i in range(len(matrixValues)):
            try: 
                print('**********************************')
                print(matrixValues[i][0],matrixValues[i][1] in  re.sub(r'[:;,.]', '', dataJson[especies][especie][path]))
                print('valor de matriz',matrixValues[i][1])
                print('valor del json',re.sub(r'[:;,.]', '', dataJson[especies][especieName][path]),dataJson[especies][especie])
            except KeyError: 
                print(matrixValues[i][0],'No existe la parte en el insecto')'''
