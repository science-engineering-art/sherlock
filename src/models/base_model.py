from typing import List
from abc  import abstractmethod
from models.corpus import Corpus
from models.document import Document


class BaseModel:

    def __init__(self, corpus: Corpus):
        self.corpus = corpus

    @abstractmethod
    def search(self, query: str) -> List[Document]: 
        pass