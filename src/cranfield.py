from qrels import QRels


class CranfieldQRels(QRels):
    def __init__(self):
        super().__init__('cranfield')

    def relevancy_criterion(relevance: int):
        if relevance in (2, 3, 4):
            return True
        return False


cranfield = CranfieldQRels()

max = -1
searchs = {}

for adj in range(1, 2):
    RR = RI = NR = NI = 0
    count = 0

    for query in cranfield.dataset.queries_iter():
        
        for _, doc_id in cranfield.results[query.query_id]:
            if cranfield.qrels[query.query_id] == 0 or count > adj: continue

            count += 1

            if doc_id in cranfield.qrels[query.query_id]:
                if cranfield.qrels[query.query_id][doc_id] in (-1 , 1):
                    RI += 1
                elif cranfield.qrels[query.query_id][doc_id] in (2, 3, 4):
                    RR += 1
            else:
                RI += 1

    P = RR/(RR + RI)
    R = RR/(cranfield.REL)
    F1 = 2/(1/P + 1/R) 
    
    if F1 > max: 
        max = F1

    print(P)
    print(adj, F1)

print(f'F1: {max}')
