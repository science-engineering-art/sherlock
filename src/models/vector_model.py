import spacy
from math import log
from models.dict import Dict
from typing import List, Tuple
from collections import Counter
from models.corpus import Corpus
from models.document import Document
from models.base_model import BaseModel

NLP = spacy.load('en_core_web_sm')

class VectorModel(BaseModel):

    def __init__(self, corpus: Corpus):
        super().__init__(corpus)
        
        # matrix of the TF of each term in each document
        self.tfs: Dict = {}
        # IDF vector
        self.idfs: Dict = {}
        
        # weight of each term in each document
        self.weights: Dict = Dict()
        # document vector norms
        self.norms: Dict = Dict()
        
        # calculation of the weights of each term in each document
        self.__calculate_weights()
    
    def search(self, query: str) -> List[Tuple[float, Document]]:
        """
            Search for the most relevant set of documents in the corpus and 
            their ranking, given a specific query.
        """
        
        # build the query vector
        query_vector = Dict(Counter([ word.lemma_ for word in NLP(query) 
                        if word.pos_ == 'NOUN']))

        # calculation of the TF of the query vector
        tf = Dict(); a = 0.4
        VectorModel.__calculate_tf(query_vector, tf)

        # calculation of the weights of the query vector
        weights = Dict()
        norm = 0
        for t in query_vector:
            weights[t] = (a + (1-a)*tf[-1, t]) * self.idfs[t]
            norm += weights[t] ** 2
        norm = norm ** (1/2)

        # cosine similarity calculation
        sims = []
        for doc in self.corpus:
            sim = 0 
            n = self.norms[doc.doc_id] * norm            
            
            if n == 0: continue
            
            for term in query_vector:
                # if self.weights[doc,term] != 0 and weights[term] != 0:
                    # print(doc.title)
                    # print(doc.text)
                    # for t in doc.terms:
                    #     print(t,doc.terms[t])
                    # print(f'weigths {self.weights[doc,term]} -- {weights[term]}')
                    # print(f'tfs {self.tfs[doc,term]} idf {self.idfs[term]}')
                sim += self.weights[doc.doc_id, term] * weights[term] / n
            sims.append((sim, doc))

        return [i for i in sorted(sims, key=lambda x: x[0], reverse=True)]

    def __calculate_tf(
            terms, 
            tfs, 
            doc_id = -1
        ):
        """
            Calculation of TF for each term in a document.
        """
        max_freq = -1
        for t in terms:
            max_freq = max(max_freq, terms[t])

        for t in terms:
            tfs[doc_id, t] = terms[t] / max_freq

    def __calculate_tfs(self):
        """
            Calculation of the TFs of each term in all the documents 
            of the corpus.
        """
        for doc in self.corpus.docs:
            VectorModel.__calculate_tf(
                doc.terms, self.tfs, doc.doc_id)

    def __calculate_idf(self):
        """
            Calculation of the IDF vector of the corpus document set.
        """
        term_docs = Dict()
        for doc in self.corpus:
            marked = Dict()
            for t in doc:
                if marked[t] == 0: 
                    term_docs[t] += 1
                    marked[t] = 1

        for t in term_docs:
            self.idfs[t] = log(len(self.corpus) / term_docs[t], 2)

    def __calculate_weights(self):
        """
            Calculation of the weights of each term in each document.
        """
        self.__calculate_tfs()
        self.__calculate_idf()
        for k in self.tfs:
            print(k, self.tfs[k])

        for doc in self.corpus:
            for term in doc:
                self.weights[doc.doc_id,term] = self.tfs[doc.doc_id,term] * self.idfs[term]
                # print(f"{self.tfs[doc.doc_id,term] * self.idfs[term]} = {self.tfs[doc.doc_id,term]} * {self.idfs[term]}")
                self.norms[doc.doc_id] += self.weights[doc.doc_id,term] ** 2
            self.norms[doc.doc_id] = self.norms[doc.doc_id] ** (1/2)
