from abc import abstractmethod
import ir_datasets
import dictdatabase as ddb
from models.base_model import BaseModel


class QRels:

    def __init__(self, model: BaseModel, dataset: str) -> None:
        
        self.dataset = ir_datasets.load(dataset)
        self.model = model
        
        s = ddb.at(f'{dataset}_QRels')
        if s.exists():
            queries = s.read()
            self.results = queries['results']
            self.rels = queries['rels']
        else:
            self.results = self.build_qresults()
            self.rels = self.build_qrels()
            s.create({
                'rels': self.rels,
                'results': self.results
            })

        self.REL = self.rels['rels']
        self.IREL = self.rels['irels']
        self.qrels = self.rels['qrels']

    @abstractmethod
    def get_query(self, query):
        pass

    def build_qresults(self):
        searchs = {}
        query_id = 1

        for query in self.dataset.queries_iter():
            searchs[str(query_id)] = {} 

            for score, doc_id in self.model.search(self.get_query(query)):
                searchs[str(query_id)][doc_id] = score
            
            print(f'QUERY: {query_id} - {query.query_id} -- {query.text} !!!!')
            print(query)
            query_id += 1

        return searchs


    def build_qrels(self):

        REL = IREL = 0
        qrels = {}

        for qrel in self.dataset.qrels_iter():
            if not qrel.query_id in qrels:
                qrels[qrel.query_id] = {}
            print(qrel.query_id)
            qrels[qrel.query_id][qrel.doc_id] = qrel.relevance
            if self.relevancy_criterion(qrel.relevance):
                REL += 1
            else:
                IREL += 1

        return {
            "rels": REL,
            "irels": IREL,
            "qrels": qrels
        } 

    def get_results(self, query_id):
        if query_id not in self.results: yield

        queries = [ (rel, doc_id) for doc_id, rel 
            in self.results[query_id].items() ]
        
        for _, doc_id in sorted(queries, key=lambda x: x[0], reverse=True):
            yield doc_id

    @abstractmethod
    def relevancy_criterion(relevance: int):
        pass

    def precision_measurements(self, amount_docs: int, amount_queries: int):

        max = (-1,-1)
        k_rank_F1 = {}

        for k in range(1, amount_docs + 1):
            RR = RI = 0    

            for query_id in range(1, amount_queries + 1):
                count = 0
                query_id = str(query_id)

                for doc_id in self.get_results(query_id):
                    if count > k: break

                    count += 1
                    if doc_id in self.qrels[query_id]:
                        if self.relevancy_criterion(self.qrels[query_id][doc_id]):
                            RR += 1
                        else:
                            RI += 1

            P = RR/(RR + RI)
            R = RR/(self.REL)

            if P == 0 or R == 0: continue
    
            F1 = 2/(1/P + 1/R) 
    
            if F1 > max[1]: 
                max = (k,F1)
            print(f'RR: {RR} RI: {RI}')
            print(f'iter: {k} P: {P} R:{R} F1: {F1}')
            k_rank_F1[str(k)] = {
                "P": P,
                "R": R,
                "F1": F1
            }

        index, F1 = max

        k_rank_F1['max'] = {
            "index": index,
            "F1": F1
        }

        ddb.at(f'k_rank_F1_{self.model.corpus.get_dataset_name}')\
            .create(k_rank_F1)
