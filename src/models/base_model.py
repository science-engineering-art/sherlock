from typing import List
from abc  import abstractmethod
from models.document import Document


class BaseModel:

    def __init__(self, dataset: str):
        self.corpus = Document.load_corpus(dataset)

    @abstractmethod
    def search(self, query: str) -> List[Document]: 
        pass