from core.models.common.dict import Dict
from core.models.vector_model import VectorModel


class RelevanceFeedback:

    def __init__(self, model: VectorModel, 
        alpha: int = 1, beta: int = 0.75, ganma: int = 0.15):

        self.model = model

        self.alpha = alpha
        self.beta = beta
        self.ganma = ganma
        
        self.queries = {}

    def search(self, query: str):
        norm = 0
        for term in self.queries[query]['weights']:
            norm += self.queries[query]['weights'][term] ** 2
        self.queries[query]['norm']= norm ** (1/2)

        return self.model.calculate_similarity(
            self.queries[query]['query_vector'],
            self.queries[query]['weights'],
            self.queries[query]['norm']
        )        

    def add_relevance(self, query: str, doc_id: str, is_relevant: bool = True):

        if query not in self.queries:
            self.queries[query] = {
                'query_vector': Dict(),
                'weights': Dict(),
                'norm': 0,
                'doc_rel': set(),
                'doc_nrel': set()
            }
            query_vector, weights, norm = self.model.query_preprocessing(query)
            self.queries[query]['query_vector'] = query_vector
            self.queries[query]['weights'] = weights
            self.queries[query]['norm'] = norm

            for term in self.model.idfs:
                self.queries[query]['query_vector'][term] = 0
                self.queries[query]['weights'][term] = 0

        elif doc_id in self.queries[query]['doc_rel'] or \
            doc_id in self.queries[query]['doc_nrel']: return

        if is_relevant:
            self.queries[query]['doc_rel'].add(doc_id)
        else:
            self.queries[query]['doc_nrel'].add(doc_id)

        self.rocchio_algorithm(query)

    def rocchio_algorithm(self, query: str):

        if len(self.queries[query]['doc_rel']) > 0:

            for term in self.queries[query]['weights']:

                self.queries[query]['weights'][term] = (self.alpha 
                    * self.queries[query]['weights'][term] 
                    + (self.beta / len(self.queries[query]['doc_rel'])) 
                    * sum(
                        [
                            self.model.weights[doc, term]
                            for doc in self.queries[query]['doc_rel']
                        ]
                    )
                )

        if len(self.queries[query]['doc_nrel']) > 0:

            for term in self.queries[query]['weights']:
               
                self.queries[query]['weights'][term] = (self.alpha 
                    * self.queries[query]['weights'][term] 
                    - (self.ganma / len(self.queries[query]['doc_nrel'])) 
                    * sum(
                        [
                            self.model.weights[doc, term]
                            for doc in self.queries[query]['doc_nrel']
                        ]
                    )
                )   
