from typing import List
from abc  import abstractmethod
from models.document import Document
from models.search_item import SearchItem


class BaseModel:

    def __init__(self, path: str):
        self.corpus = Document.load_corpus(path)

    @abstractmethod
    def search(self, query: str) -> List[SearchItem]: 
        pass