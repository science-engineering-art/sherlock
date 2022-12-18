from abc import abstractmethod
from typing import List, Tuple

import dictdatabase as ddb

from models.corpus import Corpus
from models.document import Document


class BaseModel:

    def __init__(self, corpus: Corpus):
        self.corpus = corpus
        dataset = self.corpus.dataset.__dict__['_constituents']\
            [0].__dict__['_dataset_id']
        json = f'{self.__class__.__name__}/{dataset}/preprocessing'
        
        if not ddb.at(json).exists():
            self.corpus.load_docs()
            self.preprocessing()
            self.corpus.clean()
            self.secure_storage()
        else:
            self.secure_loading()

    @abstractmethod
    def preprocessing(self):
        """
            Preprocessing that is performed before using the model employed.
        """
        pass

    @abstractmethod
    def secure_loading(self):
        """
            Secure loading of pre-calculated data.
        """
        pass

    @abstractmethod
    def secure_storage(self):
        """
            Secure storage of pre-calculated information.
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Tuple[float, str]]: 
        """
            Search for the most relevant set of documents in the corpus, 
            given a specific query.
        """
        pass