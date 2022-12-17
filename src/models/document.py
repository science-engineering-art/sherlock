import re
from typing import List
from unidecode import unidecode
from collections import Counter
from models.dict import Dict


class Document:
    def __init__(self, doc):        
        self.doc_id = doc.doc_id

        # tokenization and standardization 
        if 'text' in doc._fields:
            self.dict = Dict(Counter(self.tokenizer(doc.text)))
        elif 'abstract' in doc._fields:
            self.dict = Dict(Counter(self.tokenizer(doc.abstract)))

    def tokenizer(self, text) -> List[str]:
        return [ unidecode(word.lower()) for word in 
            re.findall(r"[\w']+", text) ]
    
    def __getitem__(self, key):
        return self.dict[key]

    def __iter__(self):
        return iter(self.dict)
