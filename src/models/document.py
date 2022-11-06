import os
import re
from typing import List
from unidecode import unidecode
from models.paragraph import Paragraph


class Document:

    @staticmethod
    def upload_document(path: str) -> List[Paragraph]:
        
        doc = open(path, 'r').read() # read file
        terms = re.split(' |\n', doc) # split by spaces and '\n'
        terms = [term for term in terms if term != ''] # remove empty terms
        
        count = 0; new_paragraph = []; paragraphs = []

        for term in terms:
            count += 1
            new_paragraph.append(term)

            if count % 20 == 0:
                paragraphs.append(' '.join(new_paragraph)) 
                new_paragraph = []       
        else:
            if new_paragraph != []:
                paragraphs.append(' '.join(new_paragraph))

        return [Paragraph(path, par) for par in paragraphs]

    @staticmethod
    def load_corpus(path: str) -> List[Paragraph]: 

        corpus: List[Paragraph] = [ par
            for file in os.listdir(path) if file != '.gitkeep'
            for par in Document.upload_document(f"{path}/{file}")]

        corpus = [paragraph for paragraph in corpus if len(paragraph.terms) > 10]
 

        return corpus