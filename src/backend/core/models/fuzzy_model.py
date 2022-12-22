import dictdatabase as ddb
from time import time
from core.models.boolean_model import BooleanModel


class FuzzyModel(BooleanModel):


    def search(self, query: str):
        processed_query = super().process_query(query)
        recovered = []
        
        for doc_id in self.docs_dict:
            product = 1.0
            for cc in processed_query:      #foreach conjuntive component
                factor_cc = 1.0
                for term_i in cc:       
                    negated = False
                    membership = 0.0
                    if term_i[0] == '~':
                        negated = True
                        term_i = term_i[1:]
                    membership = self.__get_membership(term_i, doc_id)
                    if negated:
                        membership = 1.0 - membership
                    factor_cc *= membership
                product *= (1 - factor_cc)
            sim = 1.0 - product
            recovered.append((sim, doc_id))

        return [i for i in sorted(recovered, 
                key=lambda x: x[0], reverse=True)]

    def __get_membership(self, term_i, doc_id):
        '''calculate the membership degree of a document to 
        a term's fuzzy set'''
        
        #If previously calculated
        if self.membership_degree.get((term_i,doc_id)) != None:
            return self.membership_degree.get((term_i,doc_id))
        
        product = 1.0
        terms = self.docs_dict[doc_id]
        for term_l in terms:
            correlation = self.__calculateCorrelationFactor(term_i, term_l)
            product*= (1.0 - correlation)

        membership = 1.0 - product

        #memorize the result
        self.membership_degree[(term_i, doc_id)] = membership

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
        
        #If no previously calculated. Calcule it..
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

        return c_i_l

    def precalculateConex(self):
        '''Precalculate the correlation between any pair of words in the corpus'''
        
        pair_term_freq = {}
        term_freq = {str : int}
        for doc_id in self.docs_dict:
            terms = self.docs_dict[doc_id]
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
            self.keyword_conex[("".join([term_i, ' ',term_j]))] = float(n_i_j) / (n_i + n_j - n_i_j)

        self.keyword_conex_precalculated = True




    def precalculateMembershipDegree(self):
        pass


    def secure_loading(self):
        dataset = self.corpus.get_dataset_name
        json = f'{self.__class__.__name__}/{dataset}/preprocessing'
        s = ddb.at(json)
        
        self.postprocessing()
        
        data = s.read()
        self.keyword_conex = data['keyword_conex']
        self.docs_dict  = data['docs_dict']
        for doc_id in self.docs_dict:
            self.docs_dict[doc_id] = set(self.docs_dict[doc_id])
        self.keyword_conex_precalculated = True
        
        print('......Precalculations not needed.....')
    
    def secure_storage(self):
        dataset = self.corpus.get_dataset_name
        json = f'{self.__class__.__name__}/{dataset}/preprocessing'
        s = ddb.at(json)
        
        doc_lists = {}
        for doc_id in self.docs_dict:
            list = []
            list.extend(self.docs_dict[doc_id])
            doc_lists[doc_id] = list

        
        if not s.exists():
            s.create({
                "keyword_conex": self.keyword_conex, 
                "docs_dict": doc_lists
            })

        
    def preprocessing(self):
        
        print('......Doing precalculations.....')
        
        self.postprocessing()
        
        self.docs_dict = {}
        self.keyword_conex = {}
        self.keyword_conex_precalculated = False

        for doc_id in self.corpus:
            self.docs_dict[doc_id] = set()
            for term in self.corpus[doc_id]:
                self.docs_dict[doc_id].add(term)
                
        self.precalculateConex()
        print('......Done with precalculations.....')
        
    def postprocessing(self):
        self.operators = {}
        self.membership_degree= {}
