from typing import List

import ir_datasets

from models.document import Document


class Corpus:

    def __init__(self, dataset):
        ir_dataset = ir_datasets.load(dataset)
        self.docs: List[Document] = [ Document(doc) 
            for doc in ir_dataset.docs_iter()]
