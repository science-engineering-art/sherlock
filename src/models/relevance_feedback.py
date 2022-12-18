from models.vector_model import VectorModel

class RelevanceFeedback:

    def __init__(self, model: VectorModel, query: str, 
        alpha: int = 1, beta: int =0.75, ganma: int =0.15):

        self.model = model
        self.query_vector, self.weights, self.norm = \
            model.__query_preprocessing(query)
        self.doc_rel  = set()
        self.doc_nrel = set()
        self.alpha = alpha
        self.beta = beta
        self.ganma = ganma

    def add_relevance(self, doc_id: str, is_relevant: bool = True):

        if is_relevant:
            self.doc_rel.add(doc_id)
        else:
            self.doc_nrel.add(doc_id)

        if len(self.doc_rel) > 0 and len(self.doc_nrel) > 0:

            for term in self.weights:
                self.weights[term] = (self.alpha * self.weights[term]
                    + (self.beta / len(self.doc_rel))
                    * sum(
                        [
                            self.model.weights[doc][term]
                            for doc in self.doc_rel
                            if term in self.model.weights[doc]
                        ]
                    )
                    - (self.ganma / len(self.doc_nrel))
                    * sum(
                        [
                            self.model.weights[doc_id][term]
                            for doc_id in self.doc_nrel
                            if term in self.model.weights[doc_id]
                        ]
                    )
                )

        elif len(self.doc_nrel) == 0:

            for term in self.query_vector:
                self.query_vector[term] = self.alpha * self.query_vector[term] - (self.ganma / len(self.doc_nrel)) * sum(
                    [
                        self.model.weights[doc][term]
                        for doc in self.doc_nrel
                        if term in self.model.weights[doc]
                    ]
                )

        elif len(self.doc_rel) == 0:
            
            for term in self.query_vector:
                self.query_vector[term] = self.alpha * self.query_vector[term] + (self.beta / len(self.doc_rel)) * sum(
                    [
                        self.model.weights[doc][term]
                        for doc in self.doc_rel
                        if term in self.model.weights[doc]
                    ]
                )
