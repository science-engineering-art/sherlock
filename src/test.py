from sympy.logic.boolalg import to_dnf
from sympy import sympify

terms = ["a", "b", "c", "d", "e", "f"]
docs_dict = { 0 : [0, 1, 1, 0, 0, 0],
              1 : [1, 1, 1, 0, 0, 1],
              2 : [1, 0, 0, 1, 0, 1]}

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


def doc_matches_cc(cc, doc_vector, corpus_terms):
    res = 0
    for term in cc:
        for i in range(0, len(doc_vector)):
            if doc_vector[i] == 1:
                if term[0] == "~":
                    if corpus_terms[i] == term[1:]:
                        return False
                    else:
                        res += 1
                elif corpus_terms[i] == term:
                    res += 1
                    break
    if res < len(cc):
        return False
    return True


def get_docs_matches_to_query(processed_query, docs, corpus_terms):
    matches = []
    for cc in processed_query:
        for i in range (0, len(docs)):
            if doc_matches_cc(cc, docs[i], corpus_terms):
                matches.append(i)
    return matches

q = "A AND (B or ~C)"
q = " ".join(q.split())
print(q)

expression = process_query(q)
print(expression)

print(terms)
print(docs_dict)

print(doc_matches_cc(expression[1], docs_dict[2], terms))

print(get_docs_matches_to_query(expression, docs_dict, terms))

dictionary = {1: [], 2: []}

dictionary[1] += [2]
dictionary[1] += [2]

#print(dictionary[1])
