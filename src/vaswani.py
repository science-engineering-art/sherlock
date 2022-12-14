from qrels import QRels

class VaswaniQRels(QRels):
    def __init__(self):
        super().__init__('vaswani')

    def relevancy_criterion(self, relevance: int):
        return relevance == 1

vaswani = VaswaniQRels()

max = (-1,-1)
k_rank_F1 = {}

for i in range(1,10000):
    RR = RI = 0
    count = 0

    for query_id in vaswani.qrels:

        search = [(vaswani.results[query_id][doc_id], doc_id) 
            for doc_id in vaswani.results[query_id]]
        search = sorted(search, key=lambda x: x[0], reverse=True)
        
        for _, doc_id in search: 
            count += 1
            if doc_id in vaswani.qrels[query_id]:
                RR += 1
            else:
                RI += 1
            if count == i: break
  
    P = RR/(RR + RI)
    R = RR/(vaswani.REL)

    if P == 0 or R == 0: continue
    
    F1 = 2/(1/P + 1/R) 
    
    if F1 > max[1]: 
        max = (i,F1)

    print(P)
    print(i, F1)
    k_rank_F1[str(i)] = {
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
ddb.at('k_rank_F1_vaswani_basic').create(k_rank_F1)

