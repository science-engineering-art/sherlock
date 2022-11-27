from unidecode import unidecode
from models.corpus import Corpus
from typing import Dict, List, Tuple
from models.document import Document
from models.base_model import BaseModel
from sympy.logic.boolalg import to_dnf
from sympy import sympify


class BooleanModel(BaseModel):

    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

        self.dict_terms = []

        self.dict_docs = {}

        # dictionary of document collection represented as a boolean vector of its terms
        self.docs_inverted_index = {}

    def search(self, query: str) -> List[Document]:

        # Indexing all terms in corpus
        for doc in self.corpus.docs:
            for word in doc.terms:
                if word not in self.dict_terms:
                    self.dict_terms.append(word)

        print(f"Corpus terms: {self.dict_terms}")

        # Representing each document as binary vector of its terms
        amount_docs = 0
        for doc in self.corpus.docs:
            self.dict_docs[amount_docs] = doc
            self.docs_inverted_index[amount_docs] = []
            for term in self.dict_terms:
                if term in doc.terms:
                    self.docs_inverted_index[amount_docs] += [1]
                else:
                    self.docs_inverted_index[amount_docs] += [0]
            amount_docs += 1

        print(f"Docs vectors: {self.docs_inverted_index[0]}")

        # processing query
        processed_query = self.__process_query(query)
        print(f"Processed query: {processed_query}")

        doc_matches = self.get_docs_matches_to_query(processed_query, self.docs_inverted_index, self.dict_terms)
        print(f"Matches: {doc_matches}")

        return [[1, self.dict_docs[i]] for i in doc_matches]

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
        query_dnf = str(to_dnf(expression))

        # remove parenthesis from query
        query_dnf = query_dnf.replace("(", "")
        query_dnf = query_dnf.replace(")", "")

        # split by '|' to get conjunctive components (cc)
        query_dnf = query_dnf.split(" | ")

        # split each cc by '&' to get each term in it
        for i in range(0, len(query_dnf)):
            query_dnf[i] = query_dnf[i].split(" & ")

        return query_dnf

    def match_neg_term(self, term, doc_vector, corpus_terms) -> bool:
        for i in range(0, len(doc_vector)):
            if doc_vector[i] == 1 and corpus_terms[i] == term[1:]:
                return False
        return True

    def match_term(self, term, doc_vector, corpus_terms) -> bool:
        for i in range(0, len(doc_vector)):
            if doc_vector[i] == 1 and corpus_terms[i] == term:
                print(corpus_terms[i])
                return True
        return False

    def doc_matches_cc(self, cc, doc_vector, corpus_terms):
        matches = True
        for term in cc:
            if term[0] == '~':
                matches &= self.match_neg_term(term, doc_vector, corpus_terms)
            else:
                matches &= self.match_term(term, doc_vector, corpus_terms)
        return matches

    def get_docs_matches_to_query(self, processed_query, docs, corpus_terms):
        matches = []
        for cc in processed_query:
            for i in range(0, len(docs)):
                if self.doc_matches_cc(cc, docs[i], corpus_terms):
                    matches.append(i)
        print(len(matches))
        return matches