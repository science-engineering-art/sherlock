from models.corpus import Corpus
from models.fuzzy_model import FuzzyModel
from corpus_qrels import CranfieldQRels, VaswaniQRels, Cord19QRels

cranfield_Corpus = Corpus('cranfield')
cranfield_Fuzzy  = FuzzyModel(cranfield_Corpus)
cranfield_QRels  = CranfieldQRels(cranfield_Fuzzy)
cranfield_QRels.precision_measurements(amount_docs=1400, amount_queries=225,step_size = 10)

# vaswani_Corpus = Corpus('vaswani')
# vaswani_Fuzzy  = FuzzyModel(vaswani_Corpus)
# vaswani_QRels  = VaswaniQRels(vaswani_Fuzzy)
# vaswani_QRels.precision_measurements(amount_docs=11000, amount_queries=93)

# cord19_Corpus = Corpus('cord19/trec-covid/round1')
# cord19_Fuzzy  = FuzzyModel(cord19_Corpus)
# cord19_QRels  = Cord19QRels(cord19_Fuzzy)
# cord19_QRels.precision_measurements(amount_docs=51000, amount_queries=30)
