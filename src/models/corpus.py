import ir_datasets
from typing import List, Tuple
from models.dict import Dict
from models.document import Document


class Corpus:

    def __init__(self, dataset):
        ir_dataset = ir_datasets.load(dataset)
        self.dataset = dataset
        self.docs: List[Document] = [ Document(doc) 
            for doc in ir_dataset.docs_iter()]
        # count = 0
        # self.docs = []
        # for doc in ir_dataset.docs_iter():
        #     self.docs.append(Document(doc))
        #     print(count)
        #     count += 1
        #     if count == 10000:
        #         break
        self.docs = Dict({ doc: doc for doc in self.docs })
    
    def __getitem__(self, key):

        if isinstance(key, Tuple[Document]):
            # print('it is a document')
            return self.docs[key]

        if isinstance(key, Tuple[str, Document]):
            # print('it is a tuple of str-doc')
            term, doc = key
            return self.docs[doc][term]

    def __len__(self):
        return len(self.docs)

    def __iter__(self):
        return self.docs.__iter__()
