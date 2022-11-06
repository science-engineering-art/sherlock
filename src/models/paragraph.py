import re
from unidecode import unidecode 


class Paragraph:

    def __init__(self, doc_path: str, text: str):
        self.text = text
        self.doc_path = doc_path
        self.terms = [ unidecode(word.lower()) for word in 
                        re.findall(r"[\w']+",text) ]

    def __str__(self):
        return f'{self.doc_path}\n\n....{self.text}....\n\n'

