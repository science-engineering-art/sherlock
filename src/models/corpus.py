import ir_datasets
from typing import List
from models.dict import Dict
from models.document import Document, DocumentWithOnlyNouns


class Corpus(Dict):

    def __new__(cls, _):
        return super().__new__(cls)

    def __init__(self, dataset):
        self._dataset = dataset
        self.__dict__.update({ doc._doc_id: doc for doc in self.get_documents })

    @property
    def get_documents(self) -> List[Document]:
        ir_dataset = ir_datasets.load(self._dataset)
        return [ Document(doc) for doc in ir_dataset.docs_iter()]

    def __iter__(self):
        for k in self.__dict__:
            if k[0] != '_': yield k

class CorpusWithOnlyNouns(Corpus):

    @property
    def get_documents(self) -> List[Document]:
        ir_dataset = ir_datasets.load(self._dataset)
        return [ DocumentWithOnlyNouns(doc) for doc in ir_dataset.docs_iter()]
