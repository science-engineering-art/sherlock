import os
import re
from typing import List
from unidecode import unidecode


class Document:
    
    def __init__(self, path: str):
        # set title
        a = re.findall(r"[\w]+", path)
        self.path = path
        self.title = a[len(a)-2]
         
        # load text
        with open(path, "r") as source:
            self.text = [ unidecode(word.lower()) for word in 
                re.findall(r"[\w']+",source.read()) ]
    
    def __str__(self):
        return f'{self.title}\n\n {self.path}\n\n' + ' '.join(self.text)

    @staticmethod
    def load_corpus(path: str) -> List['Document']: 

        corpus = [ Document(f"{path}/{file}") 
            for file in os.listdir(path) if file != '.gitkeep']

        return corpus

