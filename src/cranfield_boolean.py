from models.corpus import Corpus
from models.boolean_model import BooleanModel
from boolean_qrels import BooleanQRels
from cranfield_qrels import CranfieldQRels

class CranfieldBooleanQrels(BooleanQRels, CranfieldQRels):
    pass

corpus = Corpus('cranfield')
model = BooleanModel(corpus)
cranfield = CranfieldBooleanQrels(model)

cranfield.precision_measurements(amount_docs=1400, amount_queries=225)
