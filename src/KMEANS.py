from multiprocessing.pool import IMapUnorderedIterator
from pydoc import doc
from matplotlib.font_manager import weight_dict
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from traitlets import FuzzyEnum

from models.boolean_model import BooleanModel
from models.corpus import Corpus
from models.fuzzy_model import FuzzyModel
from models.vector_model import VectorModel

import dictdatabase as ddb
import numpy as np

from models.vector_model import VectorModel

class VectorModelGetWeights(VectorModel):
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
        terms = set()
        docs = set()
        for doc_id, term in self.weights:
            terms.add(term)
            docs.add(doc_id)
             
        doc_postion = {}
        term_postion = {}
        sparse_matrix = [[0.0 for _ in range(len(terms))] for _ in range(len(docs))]
        
        terms = [term for term in terms]
        for i in range(len(terms)):
            term_postion[terms[i]] = i
            
        docs = [doc for doc in docs]
        for i in range(len(docs)):
            doc_postion[docs[i]] = i
        
        for doc_id, term in self.weights:
            sparse_matrix[doc_postion[doc_id]][term_postion[term]] = self.weights[doc_id, term]
                
        return (sparse_matrix, len(terms))
    
    def get_best_k(self, sparse_matrix, dimension, pos = -1, max = 20):
        dataset = model.corpus.dataset.__dict__['_constituents']\
                [0].__dict__['_dataset_id']
        json = f'{self.__class__.__name__}/{dataset}/best_k'
        
        s = ddb.at(json)
        if not s.exists():
            best_k, bests = self.calculate_best_k(sparse_matrix, dimension, max)
            s.create(
                {'best_k' : best_k,
                 'bests' : bests}
            )
            return best_k
        else:
            data = s.read()
            if pos == -1 or pos > data['cant']:
                return data['best_k']
            return data['bests'][pos]
    
    def calculate_best_k(self, sparse_matrix, dimension, max):
        best_RSS = 1e9
        k = 2
        best_k = 2
        
        bests = {}
        while k <= max:
            kmeans = KMeans(n_clusters=k, n_init= 10, init="k-means++")
            kmeans.fit(sparse_matrix)
            RSS = kmeans.inertia_
            if RSS < best_RSS:
                best_RSS = RSS
                best_k = k
            bests[str(k)] = best_k
            print('best k: ', best_k)
            k+=1
                
        print(best_k)
        return (best_k, bests)
    
corpus = Corpus('cranfield')
model = VectorModelGetWeights(corpus)
weights, dimension = model.Getweights()
model.get_best_k(weights, dimension, 19, 5)
    
     