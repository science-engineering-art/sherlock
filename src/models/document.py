import re
from typing import List, final

import ir_datasets
from unidecode import unidecode


class Document:
    
    def __init__(self, doc):
        self.doc_id = doc.doc_id
        self.text = ''
        self.title = ''
        self.author = ''
        try:
            self.text = doc.text
        except:
            pass
        try:
            self.text = doc.body.text
        except:
            pass
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
            re.findall(r"[\w']+", self.text) ]
