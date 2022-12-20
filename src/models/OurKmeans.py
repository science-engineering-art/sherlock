from cProfile import label
from sklearn.cluster import KMeans
from sympy import centroid
from cmath import sqrt

class OurKmeans():

    def __init__(self, cluster_centers_, labels_):
        self.cluster_centers_ = [[float(coord) for coord in center] for center in cluster_centers_]
        self.labels_ = [int(label) for label in labels_]
         
    def transform(self, vector):
        trans = []
        for cent in self.cluster_centers_:
            sum = 0
            for i in range(len(vector)):
                sum += (vector[i] - cent[i])**2
            trans.append(sqrt(sum))
        return trans
                