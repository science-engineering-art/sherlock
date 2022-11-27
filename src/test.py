from sympy.logic.boolalg import to_dnf
from sympy import sympify

def process_query(query):
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


def match_neg_term(term, doc_vector, corpus_terms):
    for i in range(0, len(doc_vector)):
        if doc_vector[i] == 1 and corpus_terms[i] == term[1:]:
            return False
    return True


def match_term(term, doc_vector, corpus_terms):
    for i in range(0, len(doc_vector)):
        if doc_vector[i] == 1 and corpus_terms[i] == term:
            return True
    return False


def doc_matches_cc(cc, doc_vector, corpus_terms):
    matches = True
    for term in cc:
        if term[0] == '~':
            matches &= match_neg_term(term, doc_vector, corpus_terms)
        else:
            matches &= match_term(term, doc_vector, corpus_terms)
    return matches


def get_docs_matches_to_query(processed_query, docs, corpus_terms):
    matches = []
    for cc in processed_query:
        for i in range(0, len(docs)):
            if doc_matches_cc(cc, docs[i], corpus_terms):
                matches.append(i)
    return matches


q = "A AND (B or ~C)"
q = " ".join(q.split())
print(q)

expression = process_query(q)
print(expression)

terms = ["a", "b", "c", "d", "e", "f"]
docs_dict = { 0 : [0, 1, 1, 0, 0, 0],
              1 : [1, 1, 1, 0, 0, 1],
              2 : [1, 0, 0, 1, 0, 1]}

print(terms)
print(docs_dict)

print(doc_matches_cc(expression[1], docs_dict[2], terms))

print(get_docs_matches_to_query(expression, docs_dict, terms))

dictionary = {1: [], 2: []}

dictionary[1] += [2]
dictionary[1] += [2]

dictionary[3] = []
dictionary[3] += [1]
print(dictionary[3])