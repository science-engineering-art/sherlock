from multiprocessing.pool import IMapUnorderedIterator
from pydoc import doc
from unittest import result
from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
from matplotlib.font_manager import weight_dict
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, cluster_optics_dbscan
from sklearn.metrics import silhouette_score
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from traitlets import FuzzyEnum
from models.dict import Dict
from models.boolean_model import BooleanModel
from models.corpus import Corpus
from models.fuzzy_model import FuzzyModel
from models.vector_model import VectorModel
from collections import Counter
from unidecode import unidecode
import dictdatabase as ddb
import numpy as np
import re

from models.vector_model import VectorModel
# from symbols import term

class VectorModelKMEANS(VectorModel):
    
    def __init__(self, corpus):
        super().__init__(corpus)
    
        sparse_matrix, dimension = self.Getweights()
           
        self.noClusters = self.get_best_k(sparse_matrix, dimension, 100, 100)
        self.kmeans = self.Getkmeans(self.noClusters, sparse_matrix)
        
        self.clusters = [[] for _ in range(self.noClusters)]
        for i in range(len(self.docs)):
            self.clusters[self.kmeans.labels_[i]].append(i)
            
    def Get_Docs_and_Terms(self):
        
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
        
        print(self.kmeans.predict([query_vector]))
        query_distances = self.kmeans.transform([query_vector])[0]
        best_clusters = []
        for i in range(self.noClusters):
            best_clusters.append((query_distances[i], i))
        best_clusters = sorted(best_clusters, key=lambda x: x[0], reverse=False) 
        
        results = sorted(results, key = lambda x : x[0]*1e-6 + 1/query_distances[self.kmeans.labels_[self.doc_postion[x[1]]]], reverse = True)
        for i in range(len(results)):
            x = results[i]
            x2 = x[0]*1e-6 + 1/query_distances[self.kmeans.labels_[self.doc_postion[x[1]]]]
            results[i] = (x2,x[1])
            
            
        # print(query_vector)
        return results
        
    def GetQueryVector(idfs, terms, query):
        
        query_vector = Dict(Counter([ unidecode(word.lower()) for word in 
            re.findall(r"[\w]+", query) ]))

        # calculation of the TF of the query vector
        tf = Dict(); a = 0.4
        VectorModel.__dict__['_VectorModel__calculate_tf'](query_vector, tf)

        # calculation of the weights of the query vector
        weights = Dict()
        norm = 0
        for t in query_vector:
            weights[t] = (a + (1-a)*tf[-1, t]) * idfs[t]

        query_vector_result = []
        for term in terms:
            query_vector_result.append(weights[term])
            
        return query_vector_result
        
        
    def Getweights(self):
        
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
                 'docs' : self.docs,
                 'doc_postion' : self.doc_postion,
                 'term_postion' : self.term_postion}
            )
            return (sm, dimension)
        else:
            data = s.read()
            self.terms, self.docs, self.doc_postion, self.term_postion = data['terms'],data['docs'],data['doc_postion'],data['term_postion']
            return (data['sm'], data['dimension'])
      
    def Arrange_matrix(self):
        
        sparse_matrix = [[0.0 for _ in range(len(self.terms))] for _ in range(len(self.docs))]
        
        for doc_id, term in self.weights:
            sparse_matrix[self.doc_postion[doc_id]][self.term_postion[term]] = self.weights[doc_id, term]
                
        return (sparse_matrix, len(self.terms))
    
    def get_best_k(self, sparse_matrix, dimension, pos = -1, max = 20):
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
        best_RSS = 1e9
        k = 2
        best_k = 2
        
        bests = {}
        while k <= max:
            kmeans = KMeans(n_clusters=k, n_init= 10, init="k-means++")
            kmeans.fit(sparse_matrix)
            RSS = kmeans.inertia_
            if RSS + 2 * k * dimension < best_RSS + 2 * best_k * dimension :
                best_RSS = RSS
                best_k = k
            bests[str(k)] = best_k
            print('best k: ', best_k)
            k+=1
                
        print(best_k)
        return (best_k, bests)
    
    def Getkmeans(self, k, sparse_matrix):
        kmeans = KMeans(n_clusters=k, n_init= 10, init="k-means++").fit(sparse_matrix)
        return kmeans
    
    
class KMEANS():
    def __init__(self, kmeans):
        self.kmeans = kmeans
        
    
        
corpus = Corpus('cranfield')
model = VectorModelKMEANS(corpus)
model.search('I need to use a good query')

     