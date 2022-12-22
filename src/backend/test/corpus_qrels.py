from qrels import QRels
import dictdatabase as ddb
from core.models.base_model import BaseModel


class CranfieldQRels(QRels):
    def __init__(self, model: BaseModel):
        if model.corpus.get_dataset_name != 'cranfield':
            raise Exception()
        super().__init__(model, 'cranfield')

    def get_query(self, query):
        return query.text

    def relevancy_criterion(self, relevance: int):
        if relevance in (2, 3, 4):
            return True
        return False


class VaswaniQRels(QRels):
    def __init__(self, model: BaseModel):
        if model.corpus.get_dataset_name != 'vaswani':
            raise Exception()
        super().__init__(model, 'vaswani')

    @staticmethod
    def get_query(query):
        return query.text

    @staticmethod
    def relevancy_criterion(relevance: int):
        return relevance == 1
    
    
class Cord19QRels(QRels):
    def __init__(self, model: BaseModel):
        if model.corpus.get_dataset_name != 'cord19/trec-covid/round1':
            raise Exception()
        super().__init__(model, 'cord19/trec-covid/round1')

    def get_query(self, query):
        return ' '.join([query.title, query.description, query.narrative])

    def relevancy_criterion(self, relevance: int):
        if relevance in (1, 2):
            return True
        return False
