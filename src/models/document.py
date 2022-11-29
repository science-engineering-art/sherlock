import re
import ir_datasets
from typing import List, Tuple
from unidecode import unidecode
import spacy
from collections import Counter
from models.dict import Dict

NLP = spacy.load('en_core_web_sm') 

class Document:
    
    def __init__(self, doc):
        self.doc_id = doc.doc_id
        self.text = doc.text
        self.author = ''
        self.title = ''
        if 'author' in doc._fields:
            self.author = doc.author
        if 'title' in doc._fields:
            self.title = doc.title
        # tokenization and standardization 
        self.terms = [ word.lemma_ for word in NLP(doc.text) if word.pos_ == 'NOUN']
        self.terms = Dict(Counter(self.terms))

    def __getitem__(self, key: Tuple[str]):
        if isinstance(key, Tuple[str]):
            return self.terms[key]
    
    def __iter__(self):
        return self.terms.__iter__()

