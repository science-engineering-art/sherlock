import re
from typing import Dict, List, Tuple

from sympy import sympify
from sympy.logic.boolalg import to_dnf
from unidecode import unidecode

from models.base_model import BaseModel
from models.corpus import Corpus
from models.document import Document


class BooleanModel(BaseModel):

    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

        self.operators = {"and": "&",
                          "or": "|",
                          "not": "~"}
        self.keywords = ["as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "else",
                        "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda",
                        "nonlocal", "pass", "raise", "return", "try", "while", "with", "yield", "false", "true", "input",
                         "output", "with", "of", "so", "composite", "reduced", "re-entry", "re"]

       
        # list containing all terms in corpus
        self.dict_terms = set()

        # dictionary int -> Document of all documents in corpus
        self.dict_docs = {}

        # dictionary of document collection represented as a boolean vector of its terms
        self.docs_inverted_index = {}
         


        # Indexing all terms in corpus
        for doc in self.corpus.docs:
            for word in doc.terms:
                self.dict_terms.add(word)

        # print(f"Corpus terms: {self.dict_terms}")

        # Representing each document as binary vector of its terms
        amount_docs = 0
        for doc in self.corpus.docs:
            self.dict_docs[amount_docs] = doc
            self.docs_inverted_index[amount_docs] = set()
            for term in doc.terms:
                self.docs_inverted_index[amount_docs].add(term)
            amount_docs += 1

    def search(self, query: str):

        # processing query
        processed_query = self.process_query(query)
        print(f"Processed query: {processed_query}")

        doc_matches = self.get_docs_matches_to_query(processed_query, self.docs_inverted_index, self.dict_terms)
        print(f"Matches: {doc_matches}")

        return [[1, self.dict_docs[i]] for i in doc_matches]

    def process_query(self, query: str):

        print('raw query:', query)          #debugging

        # set to lowercase and remove unnecessary blank spaces from query
        query = " ".join(query.split()).lower()

        # remove unwanted characters
        query = re.findall(r"\)|\(|\||&|~|[\w]+", query)

        # decorate all words but important ones
        for i in range(0, len(query)):
            if query[i] not in ['or', 'and', '|', '&', '(', ')', '~']:
                query[i] = "kw_" + query[i]

        query = " ".join(query)

        # remove spaces between parenthesis and its content
        query = query.replace("( ", "(")
        query = query.replace(" )", ")")

        query = query.split(" ")

        # convert logical operands to '&', '|' or '~' (the ones sympy uses) if necessary
        # and add '&' between words with no operand between them
        i = 0
        while i != len(query):
            if query[i] in self.operators.keys():
                query[i] = self.operators[query[i]]
                if query[i].startswith("~") and not (query[i - 1].endswith("&") or query[i - 1].endswith("|")):
                    query[i - 1] += "&" + query[i]
                    query.__delitem__(i)
                i += 1
            elif i != len(query) - 1 and query[i] not in self.operators.values() and \
                    query[i + 1] not in self.operators.keys() and query[i + 1] not in self.operators.values() \
                    and not (query[i + 1].startswith("|") or query[i + 1].startswith("&")):
                query[i] += "&" + query[i + 1]
                query.__delitem__(i + 1)
            else:
                i += 1
                
        query = " ".join(query)

        # we use try except here, in case the logical expression of the query was not a valid one
        try:
            # sympify converts a string into a logical expression
            expression = sympify(query)
        except:
            return TypeError("Invalid logical expression.")

        # convert query expression into disjunctive normal form, and then convert back to string
        query_dnf = str(to_dnf(expression))

        # remove decoration in keywords
        query_dnf = query_dnf.replace("kw_", "")
        # remove parenthesis from query
        query_dnf = query_dnf.replace("(", "")
        query_dnf = query_dnf.replace(")", "")

        # split by '|' to get conjunctive components (cc)
        query_dnf = query_dnf.split(" | ")

        # split each cc by '&' to get each term in it
        for i in range(0, len(query_dnf)):
            query_dnf[i] = query_dnf[i].split(" & ")

        return query_dnf

    # matches a negated term of a conjunctive component to a document
    def match_neg_term(self, term, doc_vector, corpus_terms) -> bool:
        if term in doc_vector:
            return False
        return True
        

    # matches a simple term of a conjunctive component to a document
    def match_term(self, term, doc_vector, corpus_terms) -> bool:
        if term in doc_vector:
            return True
        return False

    # matches a conjunctive component to a document
    def doc_matches_cc(self, cc, doc_vector, corpus_terms):
        matches = True
        for term in cc:
            if term[0] == '~':
                matches &= self.match_neg_term(term, doc_vector, corpus_terms)
            else:
                matches &= self.match_term(term, doc_vector, corpus_terms)
        return matches

    # finds all matches of the query to the documents
    def get_docs_matches_to_query(self, processed_query, docs, corpus_terms):
        matches = []
        for cc in processed_query:
            for i in range(0, len(docs)):
                if self.doc_matches_cc(cc, docs[i], corpus_terms):
                    matches.append(i)
        return matches