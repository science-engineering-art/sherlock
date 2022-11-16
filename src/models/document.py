import re
import ir_datasets
from typing import List
from unidecode import unidecode

class Document:
    
    def __init__(self, doc):
        self.doc_id = doc.doc_id
        self.text = doc.text
        self.title = doc.title or None
        self.author = doc.author or None

        # tokenization and standardization 
        self.terms = [ unidecode(word.lower()) for word in 
            re.findall(r"[\w']+", doc.text) ]
