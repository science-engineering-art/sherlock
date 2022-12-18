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
    
def kmeans(sparse_matrix, dimension):
    best_RSS = 1e9
    k = 2
    best_k = 2
    
    while k < 20:
        kmeans = KMeans(n_clusters=k, init="k-means++")
        kmeans.fit(sparse_matrix)
        RSS = kmeans.inertia_
        if RSS < best_RSS:
            best_RSS = RSS
            best_k = k
        k+=1
            
    print(best_k)
    
cranfield = Corpus('cranfield')
model = VectorModelGetWeights(cranfield)
weights, dimension = model.Getweights()
kmeans(weights, dimension )
    
     