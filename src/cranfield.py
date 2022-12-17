from qrels import QRels


class CranfieldQRels(QRels):
    def __init__(self):
        super().__init__('cranfield')

    def get_query(self, query):
        return query.text

    def relevancy_criterion(self, relevance: int):
        if relevance in (2, 3, 4):
            return True
        return False

cranfield = CranfieldQRels()

max = (-1,-1)
searchs = {}
k_rank_F1 = {}

for k in range(1, 1401):
    RR = RI = 0    

    for query_id in range(1, 226):
        count = 0
        query_id = str(query_id)

        for doc_id in cranfield.get_results(query_id):
            if count > k: break

            count += 1
            if doc_id in cranfield.qrels[query_id]:
                if cranfield.qrels[query_id][doc_id] in (-1 , 1):
                    RI += 1
                elif cranfield.qrels[query_id][doc_id] in (2, 3, 4):
                    RR += 1

    P = RR/(RR + RI)
    R = RR/(cranfield.REL)

    if P == 0 or R == 0: continue
    
    F1 = 2/(1/P + 1/R) 
    
    if F1 > max[1]: 
        max = (k,F1)
    print(f'RR: {RR} RI: {RI}')
    print(f'iter: {k} P: {P} R:{R} F1: {F1}')
    k_rank_F1[str(k)] = {
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
ddb.at('k_rank_F1_cranfield_basic').create(k_rank_F1)

