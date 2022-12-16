from statistics import correlation
from pyparsing import null_debug_action
from traitlets import default
from unidecode import unidecode
from models.boolean_model import BooleanModel
from models.corpus import Corpus
from typing import Dict, List, Tuple
from models.document import Document
from models.base_model import BaseModel
from sympy.logic.boolalg import to_dnf
from sympy import product, sympify, true
import re
import dictdatabase as ddb

class FuzzyModel(BooleanModel):

    def __init__(self, corpus : Corpus, corpuse_name):


        self.corpus = corpus
        self.operators = {"and": "&",
                          "or": "|",
                          "not": "~"}

        self.docs_dict = {}
        self.membership_degree= {}
        self.keyword_conex = {}
        self.keyword_conex_precalculated = False


        for doc in corpus.docs:
            self.docs_dict[doc] = set()
            for term in doc.terms:
                self.docs_dict[doc].add(term)

        s = ddb.at(f'{corpuse_name}_FuzyModelPrecalculus')
        if s.exists():
            data = s.read()
            self.keyword_conex = data['keyword_conex']
            self.keyword_conex_precalculated = True
        else:
            self.precalculateConex()
            s.create({'keyword_conex' : self.keyword_conex})
        # self.precalculateMembershipDegree()



        print('done precalculus')                                                   #Debugging

    def search(self, query: str) -> List[Tuple[float, Document]]:
        # print('here')                                                 #Debugging
        processed_query = super().process_query(query)
        print(processed_query)                                                      #Debugging           
        recovered = []
        for doc in self.docs_dict:
            terms = self.docs_dict[doc]
            product = 1.0
            for cc in processed_query:
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
            sim = 1.0 - product
            # print(product)                                            #Debugging
            recovered.append((sim, doc))

        return [i for i in sorted(recovered, 
                key=lambda x: x[0], reverse=True)]

    def __get_membership(self, term_i, doc) -> float:
        if self.membership_degree.get((term_i,doc)) != None:
            return self.membership_degree.get((term_i,doc))
        
        product = 1.0
        terms = self.docs_dict[doc]
        # print('aqui2')                                        #Debugging
        for term_l in terms:
            correlation = self.__calculateCorrelationFactor(term_i, term_l)
            product*= (1.0 - correlation)

        membership = 1.0 - product

        self.membership_degree[(term_i, doc)] = membership

        # print('membership', membership)                               #Debugging

        return membership

    def __calculateCorrelationFactor(self, term_i, term_l) -> float:
        if self.keyword_conex.get("".join([term_i, ' ',term_l])) != None:
            return self.keyword_conex.get("".join([term_i, ' ',term_l]))
        if self.keyword_conex.get("".join([term_l, ' ',term_i]))  != None:
            return self.keyword_conex.get("".join([term_l, ' ',term_i]))
        
        if self.keyword_conex_precalculated == True:
            return 0.0
        
        # print('corrrelation factor', term_i, term_l)                            #Debugging
        

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
        self.keyword_conex["".join([term_i, ' ',term_l])] = c_i_l

        # print('c_i_l', c_i_l)                         #Debugging
        return c_i_l

    def precalculateConex(self):

        # print('corrrelation factor')                   #Debugging
        pair_term_freq = {}
        term_freq = {str : int}
        for doc in self.docs_dict:
            terms = self.docs_dict[doc]
            for term in terms:
                term_freq.setdefault(term, 0)
                term_freq[term] += 1
                for term_j in terms:
                    pair_term_freq.setdefault((term, term_j), 0)
                    pair_term_freq[(term, term_j)] += 1

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
