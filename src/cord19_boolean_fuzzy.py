from qrels import QRels


class Cord19QRels(QRels):
    def __init__(self):
        super().__init__('cord19/trec-covid/round1')

    def get_query(self, query):
        return ' '.join([query.title, query.description, query.narrative])

    def relevancy_criterion(self, relevance: int):
        if relevance in (1, 2):
            return True
        return False



cord19 = Cord19QRels()

max = (-1,-1)
searchs = {}
k_rank_F1 = {}

for adj in range(1, 10000):
    RR = RI = NR = NI = 0
    count = 0

    for query in cord19.dataset.queries_iter():
        
        for doc_id in cord19.results[query.query_id]:
            if query.query_id not in cord19.qrels or count > adj: break

            count += 1

            if doc_id in cord19.qrels[query.query_id] and \
                cord19.qrels[query.query_id][doc_id] in (1, 2):
                    RR += 1
            else:
                RI += 1

    P = RR/(RR + RI)
    R = RR/(cord19.REL)

    if P == 0 or R == 0: continue
    
    F1 = 2/(1/P + 1/R) 
    
    if F1 > max[1]: 
        max = (adj,F1)

    print(P)
    print(adj, F1)
    k_rank_F1[str(adj)] = {
        "P": P,
        "R": R,
        "F1": F1
    }

index, F1 = max

k_rank_F1['max'] = {
    "index": index,
    "F1": F1
}


import dictdatabase as ddb
ddb.at('k_rank_F1_cord19_nlp').create(k_rank_F1)

