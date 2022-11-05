from typing import List
from models.document import Document
from models.base_model import BaseModel
from models.search_item import SearchItem


class VectorModel(BaseModel):

    def __init__(self, path: str):
        super().__init__(path)
    
    def search(self, query: str) -> List[SearchItem]: 
        pass