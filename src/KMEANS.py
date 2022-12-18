from multiprocessing.pool import IMapUnorderedIterator
from pydoc import doc
from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
from matplotlib.font_manager import weight_dict
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
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

class VectorModelGetWeights(VectorModel):
    
    def __init__(self, corpus):
        super().__init__(corpus)
    
        self.terms = set()
        for _, term in self.weights:
            self.terms.add(term)
             
        self.terms = [term for term in self.terms]
    
    def search(self, query: str):
        results =  super().search(query)
        sparse_matrix, dimension = model.Getweights()
        kmeans = self.Getkmeans(sparse_matrix, dimension, pos = 5, max = 5)
        query_vector = VectorModelGetWeights.GetQueryVector(self.idfs, self.terms, query)
        print(query_vector)
        
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
        json = f'{self.__class__.__name__}/{dataset}/sparse_matrix'
        s = ddb.at(json)
        if not s.exists():
            sm, dimension = self.Arrange_matrix()
            s.create(
                {'sm' : sm ,
                 'dimension' : dimension}
            )
            return (sm, dimension)
        else:
            data = s.read()
            return (data['sm'], data['dimension'])
      
    def Arrange_matrix(self):
        docs = set()
        for doc_id, term in self.weights:
            docs.add(doc_id)
             
        doc_postion = {}
        term_postion = {}
        sparse_matrix = [[0.0 for _ in range(len(self.terms))] for _ in range(len(docs))]
        
        for i in range(len(self.terms)):
            term_postion[self.terms[i]] = i
            
        docs = [doc for doc in docs]
        for i in range(len(docs)):
            doc_postion[docs[i]] = i
        
        for doc_id, term in self.weights:
            sparse_matrix[doc_postion[doc_id]][term_postion[term]] = self.weights[doc_id, term]
                
        return (sparse_matrix, len(self.terms))
    
    def get_best_k(self, sparse_matrix, dimension, pos = -1, max = 20):
        dataset = model.corpus.dataset.__dict__['_constituents']\
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
    
    def Getkmeans(self, sparse_matrix, dimension, pos = 19, max = 20):
        k = self.get_best_k(sparse_matrix, dimension, pos, max)
        kmeans = KMeans(n_clusters=k, n_init= 10, init="k-means++")
        return kmeans
    
corpus = Corpus('cranfield')
model = VectorModelGetWeights(corpus)
model.search('marcos y tony')

     