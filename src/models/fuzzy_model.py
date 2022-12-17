import re
from statistics import correlation
from time import time
from typing import Dict, List, Tuple

import dictdatabase as ddb
from pyparsing import null_debug_action
from sympy import product, sympify, true
from sympy.logic.boolalg import to_dnf
from traitlets import default
from unidecode import unidecode

from models.base_model import BaseModel
from models.boolean_model import BooleanModel
from models.corpus import Corpus
from models.document import Document


class FuzzyModel(BooleanModel):

    # def __init__(self, corpus : Corpus, corpuse_name):


    #     self.corpus = corpus
    #     # self.operators = {"and": "&",
    #     #                   "or": "|",
    #     #                   "not": "~"}

    #     self.precalculateMembershipDegree()
    
    #     print('done precalculus')                                                   #Debugging

    def search(self, query: str):
        # print('here')                                                 #Debugging
        # time_1 = time()                                         #Debugging
        processed_query = super().process_query(query)
        # time_2 = time()                                                             #Debugging
        # print('process query took: ', time_2 - time_1)                                            #Debugging
        
        print(processed_query)                                                      #Debugging           
        recovered = []
        for doc in self.docs_dict:
            terms = self.docs_dict[doc]
            product = 1.0
            for cc in processed_query:      #foreach conjuntive component
                # time_4 = time()                                  #Debugging
                factor_cc = 1.0
                for term_i in cc:       
                    negated = False
                    membership = 0.0
                    if term_i[0] == '~':
                        negated = True
                        term_i = term_i[1:]
                    membership = self.__get_membership(term_i, doc)
                    
                    if negated:
                        membership = 1.0 - membership
                    factor_cc *= membership
                product *= (1 - factor_cc)
                # time_5 = time()                                     #Debugging
                # print('time foreach cc took: ', time_5 - time_4)         #Debugging
            sim = 1.0 - product
            # print(product)                                            #Debugging
            recovered.append((sim, doc))
        # time_3 = time()                                       #Debugging
        # print('fuzzy model query took: ', time_3 - time_2)                            #Debugging

        # print('hereeeee')                                     #Debugging
        return [i for i in sorted(recovered, 
                key=lambda x: x[0], reverse=True)]

    def __get_membership(self, term_i, doc):
        '''calculate the membership degree of a document to 
        a term's fuzzy set'''
        
        #If previously calculated
        if self.membership_degree.get((term_i,doc)) != None:
            return self.membership_degree.get((term_i,doc))
        
        product = 1.0
        terms = self.docs_dict[doc]
        # print('aqui2')                                        #Debugging
        for term_l in terms:
            correlation = self.__calculateCorrelationFactor(term_i, term_l)
            product*= (1.0 - correlation)

        membership = 1.0 - product

        #memorize the result
        self.membership_degree[(term_i, doc)] = membership

        # print('membership', membership)                               #Debugging

        return membership

    def __calculateCorrelationFactor(self, term_i, term_l):
        '''Gives the correlation factor between two terms'''
        
        #First it check if it is already calculated
        if self.keyword_conex.get("".join([term_i, ' ',term_l])) != None:
            return self.keyword_conex.get("".join([term_i, ' ',term_l]))
        if self.keyword_conex.get("".join([term_l, ' ',term_i]))  != None:
            return self.keyword_conex.get("".join([term_l, ' ',term_i]))
        
        #If it was calculated and not stored is 0
        if self.keyword_conex_precalculated == True:
            return 0.0
        
        # print('corrrelation factor', term_i, term_l)                            #Debugging
        
        #If not previously calculated. Calcule it..
        n_i_l = 0
        n_i = 0
        n_l = 0

        for doc in self.docs_dict:
            terms = self.docs_dict[doc]
            if term_i in terms:
                n_i +=1
            if term_l in terms:
                n_l +=1
            if term_i in terms and term_l in terms:
                n_i_l +=1
        c_i_l = float(n_i_l)/(n_i + n_l - n_i_l)
        self.keyword_conex["".join([term_i, ' ',term_l])] = c_i_l #store the calculated result

        # print('c_i_l', c_i_l)                         #Debugging
        return c_i_l

    def precalculateConex(self):
        '''Precalculate the correlation between any pair of words in the corpus'''
        # print('corrrelation factor')                   #Debugging
        
        pair_term_freq = {}
        term_freq = {str : int}
        for doc in self.docs_dict:
            terms = self.docs_dict[doc]
            for term in terms:
                term_freq.setdefault(term, 0)
                term_freq[term] += 1    #counts the frequency of each term
                for term_j in terms:
                    pair_term_freq.setdefault((term, term_j), 0)
                    pair_term_freq[(term, term_j)] += 1 #counts the frequency of each pair of terms

        for term_i, term_j in pair_term_freq:       
            n_i_j = pair_term_freq[(term_i, term_j)]
            n_i = term_freq[term_i]
            n_j = term_freq[term_j]
            # if term_i == term_j and term_i == 'remaining':               #Debugging
            #     print(n_i_j, n_i, n_j)
            self.keyword_conex[("".join([term_i, ' ',term_j]))] = float(n_i_j) / (n_i + n_j - n_i_j)

        self.keyword_conex_precalculated = True




    def precalculateMembershipDegree(self):
        pass


    def secure_loading(self):
        dataset = self.corpus.dataset.__dict__['_constituents']\
            [0].__dict__['_dataset_id']
        json = f'{dataset}_{self.__class__.__name__}'
        s = ddb.at(json)
        
        data = s.read()
        self.keyword_conex = data['keyword_conex']
        self.docs_dict = data['docs_dict']
        self.keyword_conex_precalculated = True
    
    def secure_storage(self):
        dataset = self.corpus.dataset.__dict__['_constituents']\
            [0].__dict__['_dataset_id']
        json = f'{dataset}_{self.__class__.__name__}'
        s = ddb.at(json)
        
        if not s.exists():
            s.create({
                "keyword_conex": self.keyword_conex, 
                "docs_dict": self.docs_dict
            })

        
    def preprocessing(self):
        self.docs_dict = {}
        self.membership_degree= {}
        self.keyword_conex = {}
        self.keyword_conex_precalculated = False

        self.precalculateConex()

        for doc_id in self.corpus:
            self.docs_dict[doc_id] = set()
            for term in self.corpus[doc_id]:
                self.docs_dict[doc_id].add(term)