from traitlets import FuzzyEnum
from models.corpus import Corpus
from models.fuzzy_model import FuzzyModel
from cranfield_qrels import CranfieldQRels

corpus = Corpus('cranfield')
model = FuzzyModel(corpus)
cranfield = CranfieldQRels(model)

cranfield.precision_measurements(amount_docs=1400, amount_queries=225)