import sys

sys.modules[__name__].__dict__.clear()
import numpy as np
from sklearn.decomposition import PCA
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('CharValues') if isfile(join('CharValues', f))]

onlyfiles.sort()

characteristics = []

insectNames = []

charToFile = []

for path in onlyfiles:
    lineToFile = []
    partName = path.replace('.txt','')
    lineToFile.append(partName)
    print(path)
    valuesOfCharacteristic = []

    #Opening files and cleaning it
    file = open('CharValues/' + path, 'r').read()
    file = re.sub(r'[:;,.]', '', file)
    file = re.sub(path,'',file)
    file = re.sub(r'[\w ]*@','',file)
    if file != '':
        content = file.split('\n')
        #Distance matrix creation
        distanceMatrix = []
        for line in content:
            if line != '':
                lineWords = line.split()
                lon = []
                for lineAux in content:
                    if lineAux != '':
                        distance = len(set(lineWords).union(lineAux.split())) - len(
                            set(lineWords).intersection(lineAux.split()))
                        lon.append(distance)
                distanceMatrix.append(lon)
        #for r in distanceMatrix: print(r)
        #creating the plot from the distance matrix
        pca = PCA(n_components=2)
        X3d = pca.fit_transform(distanceMatrix)
        xpoints = []
        ypoints = []
        for i in range(0, len(X3d)):
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
        #creating the elbow
        X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
        colors = ['b', 'g', 'r']
        markers = ['o', 'v', 's']
        # k means determine k
        derivadas = []

        distortions = []
        K = range(1, 10)

        for k in K:
            kmeanModel = KMeans(n_clusters=k).fit(X)
            kmeanModel.fit(X)
            distortions.append(sum(np.min(
                cdist(X, kmeanModel.cluster_centers_,
                      'euclidean'), axis=1)) / X.shape[0])


        #using the central difference to obtain the exact value of k
        for t in range(1, len(distortions) - 1):
            derivadas.append(distortions[t + 1]
                             + distortions[t - 1]
                             - (2 * distortions[t]))
        # Plot the elbow
        '''plt.plot(K, distortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.show()'''

        # cluster creation
        distanceMatrix = []
        sumas = []
        distance = 0
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(file.split('\n'))
        # Add 2 to the real k due to the index and the formula
        true_k = derivadas.index(max(derivadas)) + 2

        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()

        #creating a 2-dim array to store the top terms of each cluster
        allTerms = []
        for i in range(true_k):
            termsCluster = []
            # print("Cluster %d:" % i),
            for ind in order_centroids[i, :10]:
                termsCluster.append(terms[ind])
            lineAux = ''
            for t in range(0,4):
                lineAux = lineAux + '_' + termsCluster[t]
            lineToFile.append(lineAux)
            allTerms.append(termsCluster)


        #Asigning each phrase to a cluster using its index

        for line in content:
            values = []
            intersections = []
            for cluster in allTerms:
                intersection = set(line.split()).intersection(cluster)
                if len(intersection) > 0:
                    intersections.append(intersection)
                else:
                    intersections.append(0)
                values.append(len(intersection))
            maxValue = max(values)

            if maxValue == 0:
                valuesOfCharacteristic.append('?')
            else:
                repeatedIndex = []
                for elem in range(0,len(values)):
                    if values[elem] == maxValue:
                        repeatedIndex.append(elem)
                if len(repeatedIndex)> 1:
                    aditions = []
                    for auxIndex in repeatedIndex:
                        sumAux = 0
                        for word in intersections[auxIndex]:
                            sumAux += allTerms[auxIndex].index(word)
                        aditions.append(sumAux)
                    valuesOfCharacteristic.append(repeatedIndex[aditions.index(min(aditions))])
                else:
                    valuesOfCharacteristic.append(values.index(maxValue))
        characteristics.append(valuesOfCharacteristic)
        charToFile.append(lineToFile)

finalMatrix = []

for m in range(0,len(characteristics[0])):
    auxVector = []
    for n in range(0,len(characteristics)):
        auxVector.append(characteristics[n][m])
    finalMatrix.append(auxVector)

for z in range(len(finalMatrix)):
    for x in range(len(finalMatrix[z])):
        print(' '+str(finalMatrix[z][x]), end='')
    print('\n')


print(len(characteristics))
print(len(characteristics[0]))

fileInsects = open('sortedInsects.txt','r')

insectNames = fileInsects.read().split('\n')


finalFile = open('tntFile.tnt','w')

finalFile.write('nstates num 6;\n')
finalFile.write('xread\n')

finalFile.write(str(len(insectNames)))
finalFile.write(' ')
finalFile.write(str(len(finalMatrix[0])))

finalFile.write('\n\n&[num]\n')


i = j = 0


for i in range(0,len(insectNames)-1):
    finalFile.write(insectNames[i].replace(' ','_'))
    finalFile.write('\t\t')
    for j in range(0,len(finalMatrix[0])):
        finalFile.write(str(finalMatrix[i][j]))
    finalFile.write('\n')
finalFile.write(';\n\ncnames\n')

i = j = 0

for i in range(len(charToFile)):
    finalFile.write('{ '+str(i))
    for element in charToFile[i]:
        finalFile.write(' ')
        finalFile.write(element)
    finalFile.write(';\n')
finalFile.write(';')





finalFile.close()
fileInsects.close()