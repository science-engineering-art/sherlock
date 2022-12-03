from abc import abstractmethod
import ir_datasets
import dictdatabase as ddb
from models.vector_model import VectorModel
from models.corpus import CorpusWithOnlyNouns


class QRels:

    def __init__(self, dataset) -> None:
        
        self.corpus = CorpusWithOnlyNouns(dataset)
        self.model = VectorModel(self.corpus)
        self.dataset = ir_datasets.load(dataset)
        
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
            

    def build_qresults(self):
        searchs = {}

        for query in self.dataset.queries_iter():
            searchs[query.query_id] = {} 
            for score, doc_id in self.model.search(query.text):
                searchs[query.query_id][doc_id] = score
            print(f'query {query.query_id}')

        return searchs


    def build_qrels(self):

        REL = IREL = 0
        qrels = {}

        for qrel in self.dataset.qrels_iter():
            if not qrel.query_id in qrels:
                qrels[qrel.query_id] = {}
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

    @abstractmethod
    def relevancy_criterion(relevance: int):
        pass