from math import log
import re
from typing import Dict, List
from unidecode import unidecode
from models.base_model import BaseModel
from models.search_item import SearchItem


class VectorModel(BaseModel):

    def __init__(self, path: str):
        super().__init__(path)
        
        self.dict_terms = {}
        self.dict_docs = {}
        self.frequency: List[List[int]] = []
        self.tfs: List[List[float]] = []
        self.idf: List[List[float]] = []
        self.weights: List[List[float]] = []
        
        self.__calculate_weights()
    
    def search(self, query: str) -> List[SearchItem]:
        
        query_vector: List[str] = [ unidecode(word.lower()) for word in 
                                   re.findall(r"[\w']+", query) ]

        dict_query = {}


    def __calculate_tf(
            text: List[str], 
            dict_terms: Dict[str, int] = {},
            frequency: List[int] = [],
            tf: List[float] = []
        ):

        amount_terms = len(frequency)
        max_freq = -1

        for word in text:

            if not word in dict_terms:
                frequency.append(0)
                dict_terms[word] = amount_terms
                amount_terms += 1
                
            frequency[dict_terms[word]] += 1
            max_freq = max(max_freq, frequency[dict_terms[word]])

        for j in range(0, amount_terms):
            tf.append(frequency[j] / max_freq)

    def __calculate_tfs(self):

        amount_terms = 0; amount_docs = 0

        for doc in self.corpus:

            self.dict_docs[doc] = amount_docs
            self.frequency.append([0 for _ in range(0, amount_terms)])
            self.tfs.append([])

            VectorModel.__calculate_tf(
                doc.text,
                self.dict_terms,
                self.frequency[amount_docs],
                self.tfs[amount_docs]
            )
            amount_terms = len(self.frequency[amount_docs])
            amount_docs += 1

        for i in range(0, len(self.frequency)):
            while len(self.frequency[i]) < amount_terms:
                self.frequency[i].append(0)
                self.tfs[i].append(0)

        print(self.tfs[amount_docs-1])

    def __calculate_idf(self):
        
        amount_docs = len(self.corpus); amount_terms = len(self.frequency[0])

        for i in range(0, amount_terms):
            n = 0
            for j in range(0, amount_docs):
                if self.frequency[j][i] != 0:
                    n+=1
            self.idf.append(log(amount_docs / n, 2))

    def __calculate_weights(self):
        self.__calculate_tfs()
        self.__calculate_idf()

        self.weights = [[0.0 for _ in range(0, len(self.frequency[0]))] 
                           for _ in range(0, len(self.corpus))]        

        for i in range(0, len(self.corpus)):
            for j in range(0, len(self.frequency[0])):
                self.weights[i][j] = self.tfs[i][j] * self.idf[j]