import re
from sympy import sympify
from sympy.logic.boolalg import to_dnf
from models.base_model import BaseModel
from models.dict import Dict
import dictdatabase as ddb


class BooleanModel(BaseModel):

    def preprocessing(self):        
        self.doc_terms = Dict()

        for doc_id in self.corpus:
            self.doc_terms[doc_id] = Dict()

            for term in self.corpus[doc_id]:
                self.doc_terms[doc_id][f'kw_{term}'] = 1

    def secure_storage(self):
        dataset = self.corpus.get_dataset_name
        json = f'{self.__class__.__name__}/{dataset}/preprocessing'
        s = ddb.at(json)
        
        if not s.exists():
            s.create({
                "doc_terms" : {}
            })

            with ddb.at(json, key="doc_terms").session() as (session, doc_terms):
            
                for doc_id in self.doc_terms:                    
                    if not doc_id in doc_terms:
                        doc_terms[doc_id] = {}

                    for term in self.doc_terms[doc_id]:
                        doc_terms[doc_id][term] = 1

                session.write()

    def secure_loading(self):
        dataset = self.corpus.get_dataset_name
        json = f'{self.__class__.__name__}/{dataset}/preprocessing'
        s = ddb.at(json)
        
        if s.exists():
            json = s.read()
            self.doc_terms = Dict()

            for doc_id in json['doc_terms']:
                if not doc_id in self.doc_terms:
                    self.doc_terms[doc_id] = Dict()

                for term in json['doc_terms'][doc_id]:
                    self.doc_terms[doc_id][term] = 1

    def search(self, query: str):

        # processing query
        processed_query = self.process_query(query)
        print(f"Processed query: {processed_query}")

        doc_matches = self.get_docs_matches_to_query(processed_query)
        print(f"Matches: {doc_matches}")

        return [(1, doc_id) for doc_id in doc_matches]

    def process_query(self, query: str):

        print('raw query:', query)          #debugging

        query = query.replace("'", "")

        # remove unwanted characters
        query = re.findall(r"\)|\(|\||&|~|[\w]+", query)

        # decorate all words but important ones
        for i in range(0, len(query)):
            if query[i] not in ['(', ')', '|', '&', '~']:
                query[i] = "kw_" + query[i]

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
    

    # finds all matches of the query to the documents
    def get_docs_matches_to_query(self, processed_query):

        # matches a conjunctive component to a document
        def doc_matches_cc(cc, doc: Dict):
            matches = True
            for term in cc:
                if term[0] == '~':
                    matches &= (doc[term[1:]] == 0)
                else:
                    matches &= (doc[term] == 1)
            return matches

        matches = []

        for doc_id in self.doc_terms:
            # checks if the document matches any conjunctive components
            print(processed_query)
            for cc in processed_query:
                if doc_matches_cc(cc, self.doc_terms[doc_id]):
                    matches.append(doc_id)
                    break

        return matches