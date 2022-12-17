from qrels_boolean_fuzzy import QRels


class CranfieldQRels(QRels):
    def __init__(self):
        super().__init__('cranfield')

    def get_query(self, query):
        return query.text

    def relevancy_criterion(self, relevance: int):
        if relevance in (2, 3, 4):
            return True
        return False
    
    def build_qrels(self):

        REL = IREL = 0
        qrels = {}

        for qrel in self.dataset.qrels_iter():
            if not qrel.query_id in qrels:
                qrels[qrel.query_id] = {}
            qrels[qrel.query_id][qrel.doc_id] = qrel.relevance
            if self.relevancy_criterion(qrel.relevance):
                REL += 1
            else:
                IREL += 1

        return {
            "rels": REL,
            "irels": IREL,
            "qrels": qrels
        } 


cranfield = CranfieldQRels()

max = (-1,-1)
searchs = {}
k_rank_F1 = {}

for adj in range(10, 100):
    RR = RI = 0
    count = 0

    for query_id in range(3, 256):
        query_id = str(query_id)

        for doc_id in cranfield.get_results(query_id):
            if count > adj: break

            count += 1
            if doc_id in cranfield.qrels[query_id]:
                if cranfield.qrels[query_id][doc_id] in (-1 , 1):
                    RI += 1
                elif cranfield.qrels[query_id][doc_id] in (2, 3, 4):
                    RR += 1
            # else:
            #     RI += 1
            
    if RR == 0 and RI == 0: continue

    P = RR/(RR + RI)
    R = RR/(cranfield.REL)

    if P == 0 or R == 0: continue
    
    F1 = 2/(1/P + 1/R) 
    
    if F1 > max[1]: 
        max = (adj,F1)
    # print(f'RR: {RR} RI: {RI}')
    # print(f'iter: {adj} P: {P} R:{R} F1: {F1}')
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

ddb.at('k_rank_F1_cranfield_basic').create(k_rank_F1, force_overwrite= True)

