from unidecode import unidecode
from corpus import Corpus
from typing import Dict, List, Tuple
from document import Document
from base_model import BaseModel
from sympy.logic.boolalg import to_dnf
from sympy import sympify


class BooleanModel(BaseModel):

    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

        self.dict_terms = []

        # dictionary of document collection represented as a boolean vector of its terms
        self.docs_inverted_index = {}

    def search(self, query: str) -> List[Document]:

        # Indexing all terms in corpus
        for doc in self.corpus.docs:
            for word in doc:
                if word not in self.dict_terms:
                    self.dict_terms.append(word)

        # Representing each document as binary vector of its terms
        amount_docs = 0
        for doc in self.corpus.docs:
            for term in self.dict_terms:
                if term in doc:
                    self.docs_inverted_index[amount_docs] += [1]
                else:
                    self.docs_inverted_index[amount_docs] += [0]
                amount_docs += 1

        return super().search(query)

    def __process_query(self, query: str) -> TypeError | list[str]:
        # set query to lowercase
        query = query.lower()

        # convert logical operands to '&', '|' or '~' (the ones sympy uses)
        # in case they were written differently or remove blank spaces between operators and terms
        query = query.replace(" or ", "|")
        query = query.replace(" | ", "|")
        query = query.replace(" and ", "&")
        query = query.replace(" & ", "&")
        query = query.replace(" not ", "~")
        query = query.replace(" ~ ", "~")

        # if after processing the query there are still blank spaces is becuase there is
        # no operator between those terms, so we add '&' between them
        query = query.replace(" ", "&")

        # we use try except here, in case the logical expression of the query was not a valid one
        try:
            # sympify converts a string into a logical expression
            expression = sympify(query)
        except:
            return TypeError("Invalid logical expression.")

        # convert query expression into disjunctive normal form, and then convert back to string
        query_dfn = str(to_dnf(expression))

        # remove parenthesis from query
        query_dfn = query_dfn.replace("(", "")
        query_dfn = query_dfn.replace(")", "")

        # split by '|' to get conjunctive components (cc)
        query_dfn = query_dfn.split(" | ")

        # split each cc by '&' to get each term in it
        for i in range(0, len(query_dfn)):
            query_dfn[i] = query_dfn[i].split(" & ")

        return query_dfn