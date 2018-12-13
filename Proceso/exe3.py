import sys
sys.modules[__name__].__dict__.clear()
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir('CharValues') if isfile(join('CharValues', f))]

for q in range(len(onlyfiles)):
    path = onlyfiles[q]
    aux = []
    sumas = []
    distancia = 0
    file = open('CharValues/'+path,'r').read()
    if file != '':
        content = file.split('\n')
        j=i=0
        for i in range(len(content)):
            if content[i] != '':
                content[i] = re.sub(r'[:;,.]', '', content[i])
                content[i] = content[i][content[i].index('@'):].replace('@','')
            content[i] = content[i].split()
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
        # Plot the elbow
        '''plt.plot(K, distortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.show()'''
        #cluster creation
        aux = []
        sumas = []
        distancia = 0
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(file.split('\n'))
        true_k = derivadas.index(max(derivadas)) + 2
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)
        '''print("Top terms per cluster:")
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        for i in range(true_k):
            print("Cluster %d:" % i),
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind])'''

