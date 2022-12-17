from qrels import QRels
from models.base_model import BaseModel


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
