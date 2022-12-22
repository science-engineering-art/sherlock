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
                sum += (vector[i] - cent[i])*(vector[i] - cent[i])
            trans.append(sqrt(sum).real)
        return trans
    
    def ClassifyAllDocuments(self, doc_position):
        self.clusters = [[] for _ in range(len(self.cluster_centers_))]
        for i in doc_position.values():
            self.clusters[self.labels_[i]].append(i)