import ir_datasets
from typing import List
from models.dict import Dict
from models.document import Document, DocumentWithOnlyNouns


class Corpus(Dict):

    def __new__(cls, _):
        return super().__new__(cls)

    def __init__(self, dataset):
        self._dataset = ir_datasets.load(dataset)

    def load_docs(self):
        self.__dict__.update({ doc._doc_id: doc for doc in self.get_documents })
    
    def clean(self):
        clean = { '_dataset': self._dataset }
        self.__dict__.update(clean)

    @property
    def get_documents(self) -> List[Document]:
        return [Document(doc) for doc in self._dataset.docs_iter()]

    def __iter__(self):
        for doc in self.get_documents.__iter__():
            yield doc._doc_id
    
    def get_doc(self, doc_id: str):
        doc = self._dataset.docs_store().get(doc_id)
        result = { 'doc_id': '', 'title': '', 'author': '', 'text': '', 'abstract': ''}
        
        for field in result:
            if field in doc._fields:
                result[field] = eval(f'doc.{field}')
        
        return result


class CorpusWithOnlyNouns(Corpus):

    @property
    def get_documents(self) -> List[Document]:
        return [DocumentWithOnlyNouns(doc) for doc in self._dataset.docs_iter()]