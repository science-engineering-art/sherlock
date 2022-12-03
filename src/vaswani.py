from qrels import QRels

class VaswaniQRels(QRels):
    def __init__(self):
        super().__init__('vaswani')

    def relevancy_criterion(relevance: int):
        return relevance == 1

vaswani = VaswaniQRels()

RR = RI = 0
count = 0

for query_id in vaswani.qrels:
    for doc_id in vaswani.results[query_id]:        
        if doc_id in vaswani.qrels[query_id]:
            RR += 1
        else:
            RI += 1

P = RR/(RR + RI)
R = RR/(vaswani.REL)
F1 = 2/(1/P + 1/R) 
    
print(f'F1: {F1}')
