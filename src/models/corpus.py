import ir_datasets
from models.dict import Dict
from models.document import Document


class Corpus:
    def __init__(self, dataset):
        self.dict = Dict()
        self.dataset = ir_datasets.load(dataset)

    def load_docs(self):
        self.dict = Dict({ doc.doc_id: doc for doc in 
        [Document(doc) for doc in self.dataset.docs_iter()] })

    def clean(self):
        self.dict = Dict()
    
    @property
    def get_dataset_name(self) -> str:
        return self.dataset.__dict__['_constituents'][0].__dict__['_dataset_id']

    def __getitem__(self, key):
        return self.dict[key]

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)
 
    def get_doc(self, doc_id: str):
        doc = self.dataset.docs_store().get(doc_id)
        result = { 'doc_id': '', 'title': '', 'author': '', 'text': '', 'abstract': ''}
        
        for field in result:
            if field in doc._fields:
                result[field] = eval(f'doc.{field}')
        
        return result
