from models.corpus import Corpus
from models.vector_model import VectorModel
from cranfield_qrels import CranfieldQRels

corpus = Corpus('cranfield')
model = VectorModel(corpus)
cranfield = CranfieldQRels(model)

cranfield.precision_measurements(amount_docs=1400, amount_queries=225)