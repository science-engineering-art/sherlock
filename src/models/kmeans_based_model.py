from sqlite3 import SQLITE_CREATE_TRIGGER
from unittest import result
from sklearn.cluster import KMeans
from models.OurKmeans import OurKmeans
from models.dict import Dict
from models.vector_model import VectorModel
from collections import Counter
from unidecode import unidecode
import dictdatabase as ddb
import re
import matplotlib.pyplot as plt
from models.vector_model import VectorModel
from sklearn.cluster import KMeans

class VectorModelKMEANS(VectorModel):
    
    def __init__(self, corpus):
        super().__init__(corpus)
           
        self.terms, docs, self.doc_postion, self.term_postion = self.Get_Docs_and_Terms()   
        sparse_matrix, _ = self.Arrange_matrix(docs)
        print('Done preparing matrix')
           
        self.noClusters = self.get_best_k(sparse_matrix, len(self.doc_postion), 10, 10)
        print('Done obatining the best k value')
        
        print(".....Creating clusters.......")
        self.kmeans = self.Getkmeans(self.noClusters, sparse_matrix)
        print(".....Clusters created.......")
        
            
    def Get_Docs_and_Terms(self):
        '''Compute documents and terms as lists and stores it positions in a dictionary'''
        
        terms = set()
        docs = set()
        for doc_id, term in self.weights:
            docs.add(doc_id)
            terms.add(term)
             
        terms = [term for term in terms]
        docs = [doc_id for doc_id in docs]
        doc_postion = {}
        term_postion = {}
        
        for i in range(len(terms)):
            term_postion[terms[i]] = i
            
        docs = [doc for doc in docs]
        for i in range(len(docs)):
            doc_postion[docs[i]] = i
    
        return (terms, docs, doc_postion, term_postion)
    
    def search(self, query: str):
        results =  super().search(query)
        query_vector = VectorModelKMEANS.GetQueryVector(self.idfs, self.terms, query)
        
        query_distances = self.kmeans.transform(query_vector)
        best_clusters = []
        for i in range(self.noClusters):
            best_clusters.append((query_distances[i], i))
        best_clusters = sorted(best_clusters, key=lambda x: x[0], reverse=False) 
        
        min_distance = max(best_clusters[0][0] - 1, 1)
        mx_score = results[0][0]
        
        #we sort this time based in nearest clusters
        results = sorted(results, key = lambda x :   (mx_score * min_distance + x[0]*1e-1)/query_distances[self.kmeans.labels_[self.doc_postion[x[1]]]], reverse = True)
        for i in range(len(results)):
            x = results[i]
            
            #Is assigned to each document a score depending on the corresponding cluster for the document
            x2 = float((mx_score * min_distance + x[0]*1e-1)/query_distances[self.kmeans.labels_[self.doc_postion[x[1]]]])
            results[i] = (x2,x[1])
            
        return results
            
    def searchSplitedByClusters(self, query : str):
        results = self.search(query)
        
        results_by_cluster = [[] for _ in range(self.noClusters)]
        for score, doc_id in results:
            results_by_cluster[self.kmeans.labels_[self.doc_postion[doc_id]]].append((self.kmeans.labels_[self.doc_postion[doc_id]], score, doc_id))

        results_by_cluster = sorted(results_by_cluster, key=lambda x: x[0][1], reverse=True)

        return results_by_cluster
        
    def GetQueryVector(idfs, terms, query):
        '''Obtains the query in the form of a vector of the same space as the documents'''
        
        query_vector = Dict(Counter([ unidecode(word.lower()) for word in 
            re.findall(r"[\w]+", query) ]))

        # calculation of the TF of the query vector
        tf = Dict(); a = 0.4
        VectorModel.__dict__['_VectorModel__calculate_tf'](query_vector, tf)

        # calculation of the weights of the query vector
        weights = Dict()
        for t in query_vector:
            weights[t] = (a + (1-a)*tf[-1, t]) * idfs[t]

        query_vector_result = []
        for term in terms:
            query_vector_result.append(weights[term])
            
        return query_vector_result
        
    def AssignFieldsWithStorage(self):
        '''Restore or save the necesary properties in local storage'''
        
        dataset = self.corpus.dataset.__dict__['_constituents']\
            [0].__dict__['_dataset_id']
        json = f'{self.__class__.__name__}/{dataset}/other_properties'
        s = ddb.at(json)
        if not s.exists():
            self.terms, self.docs, self.doc_postion, self.term_postion = self.Get_Docs_and_Terms()
            sm, dimension = self.Arrange_matrix()
            s.create(
                {'sm' : sm ,
                 'dimension' : dimension,
                 'terms' : self.terms,
                 'doc_postion' : self.doc_postion,
                 'term_postion' : self.term_postion}
            )
            return (sm, dimension)
        else:
            data = s.read()
            self.terms,  self.doc_postion, self.term_postion = data['terms'],data['doc_postion'],data['term_postion']
            return (data['sm'], data['dimension'])
      
    def Arrange_matrix(self, docs):
        '''calculate the matrix necessary for the kmenas method, i.e. the matrix
        where each row represents the vector corresponding to a document in the 
        space of dimension len(terms)'''
        
        sparse_matrix = [[0.0 for _ in range(len(self.terms))] for _ in range(len(docs))]
        
        for doc_id, term in self.weights:
            sparse_matrix[self.doc_postion[doc_id]][self.term_postion[term]] = self.weights[doc_id, term]
                
        return (sparse_matrix, len(self.terms))
    
    def get_best_k(self, sparse_matrix, dimension, pos = -1, max = 20):
        '''get from local storage or calculate and save the best amount of clusters
        in dependency of the max amount of clusters we desire to have '''
        
        dataset = self.corpus.dataset.__dict__['_constituents']\
                [0].__dict__['_dataset_id']
        json = f'{self.__class__.__name__}/{dataset}/best_k'
        
        s = ddb.at(json)
        if not s.exists():
            best_k, bests = self.calculate_best_k(sparse_matrix, dimension, max)
            s.create(
                {'best_k' : best_k,
                 'bests' : bests,
                 'cant' : max
                }
            )
            return best_k
        else:
            data = s.read()
            if pos == -1 or pos > data['cant']:
                return data['best_k']
            return data['bests'][str(pos)]
    
    def calculate_best_k(self, sparse_matrix, dimension, max):
        '''Iterates from 2 to max to find the best amount of clusters
        based on the RSS + penality'''
        
        best_RSS = 1e9
        k = 2
        best_k = 2
        lambda_0 = 0.08 * dimension
        
        bests = {}
        while k <= max:
            kmeans = KMeans(n_clusters=k, n_init= 10, init="k-means++")
            kmeans.fit(sparse_matrix)
            RSS = kmeans.inertia_
            if RSS + lambda_0 * k < best_RSS + lambda_0 * best_k  :
                best_RSS = RSS
                best_k = k
            bests[str(k)] = best_k
            print('best k: ', best_k)
            k+=1
                
        return (best_k, bests)
    
    def Getkmeans(self, k, sparse_matrix):
        '''Load from storage the centroids and labels if 
        kmeans is stored or otherwise calculate it and store it'''
        
        dataset = self.corpus.dataset.__dict__['_constituents']\
                [0].__dict__['_dataset_id']
        json = f'{self.__class__.__name__}/{dataset}/Kmeans_object'
        
        s = ddb.at(json)
        if not s.exists():
            kmeans = KMeans(n_clusters=k, n_init= 10, init="k-means++").fit(sparse_matrix)
            kmeans2 = OurKmeans(kmeans.cluster_centers_, kmeans.labels_)
            s.create(
                {
                    'labels_' : kmeans2.labels_,
                    'cluster_centers_' : kmeans2.cluster_centers_,
                }
            )
        else:
            data = s.read()
            kmeans2 = OurKmeans(data['cluster_centers_'],  data['labels_'])
    
        return kmeans2
    
    def ElbowMethod(sparse_matrix, min, max):
        k = min
        points = []
        
        while k <= max:
            kmeans = KMeans(n_clusters=k, n_init= 10, init="k-means++")
            kmeans.fit(sparse_matrix)
            RSS = kmeans.inertia_
            points.append([k,RSS])
            k+=1
                
        VectorModelKMEANS.plot_results(points)
    
    def plot_results(inertials):
        x, y = zip(*[inertia for inertia in inertials])
        plt.plot(x, y, 'ro-', markersize=8, lw=2)
        plt.grid(True)
        plt.xlabel('Num Clusters')
        plt.ylabel('Inertia')
        plt.show()
    