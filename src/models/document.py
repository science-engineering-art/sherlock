import re
import ir_datasets
from typing import List, final
from unidecode import unidecode

class Document:
    
    def __init__(self, doc):
        self.doc_id = doc.doc_id
        self.text = doc.text
        self.title = ''
        self.author = ''
        try:
            self.title = doc.title
        except:
            pass
        try:
            self.author = doc.author
        except:
            pass

        # tokenization and standardization 
        self.terms = [ unidecode(word.lower()) for word in 
            re.findall(r"[\w']+", doc.text) ]
