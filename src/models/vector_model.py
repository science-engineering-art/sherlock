from math import log
from typing import Dict, List
from models.document import Document
from models.base_model import BaseModel
from models.search_item import SearchItem


class VectorModel(BaseModel):

    def __init__(self, path: str):
        super().__init__(path)
        
        self.dict_terms = {}
        self.dict_docs = {}
        self.frequency: List[List[int]] = []
        self.tf: List[List[float]] = []
        self.idf: List[List[float]] = []
        
        self.__calculate_tf()
        self.__calculate_idf()
    
    def search(self, query: str) -> List[SearchItem]:
        pass

    def __calculate_tf(self):

        amount_terms = 0; amount_docs=0
        maxs = [] # maximum frequency of terms in the document

        for doc in self.corpus:

            self.dict_docs[doc] = amount_docs
            self.frequency.append([0 for _ in range(0, amount_terms)])
            max_frequency_terms = -1

            for word in doc.text:
            
                if not word in self.dict_terms:
                    self.frequency[amount_docs].append(0)
                    self.dict_terms[word] = amount_terms
                    amount_terms+=1
                
                self.frequency[amount_docs][self.dict_terms[word]] += 1

                max_frequency_terms = max(max_frequency_terms, 
                    self.frequency[amount_docs][self.dict_terms[word]])
            
            maxs.append(max_frequency_terms)
            amount_docs += 1

        for doc in self.frequency:
            while len(doc) < amount_terms:
                doc.append(0)

        self.tf = [[0.0 for _ in range(0, amount_terms)] 
                    for _ in range(0, amount_docs)]

        # calculate TF
        for i in range(0, amount_docs):
            for j in range(0, amount_terms):
                tmp = self.frequency[i][j] / maxs[i]
                self.tf[i][j] = tmp

    def __calculate_idf(self):
        
        amount_docs = len(self.corpus); amount_terms = len(self.frequency[0])

        for i in range(0, amount_terms):
            n = 0
            for j in range(0, amount_docs):
                if self.frequency[j][i] != 0:
                    n+=1
            self.idf.append(log(amount_docs / n, amount_docs))