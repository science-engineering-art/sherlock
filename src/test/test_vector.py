from models.corpus import Corpus
from models.vector_model import VectorModel
from corpus_qrels import CranfieldQRels, VaswaniQRels, Cord19QRels

cranfield_Corpus = Corpus('cranfield')
cranfield_Vector = VectorModel(cranfield_Corpus)
cranfield_QRels = CranfieldQRels(cranfield_Vector)
cranfield_QRels.precision_measurements(amount_docs=1400, amount_queries=225)

vaswani_Corpus = Corpus('vaswani')
vaswani_Vector = VectorModel(vaswani_Corpus)
vaswani_QRels = VaswaniQRels(vaswani_Vector)
vaswani_QRels.precision_measurements(amount_docs=11000, amount_queries=93, step_size=2)

cord19_Corpus = Corpus('cord19/trec-covid/round1')
cord19_Vector = VectorModel(cord19_Corpus)
cord19_QRels = Cord19QRels(cord19_Vector)
cord19_QRels.precision_measurements(amount_docs=51000, amount_queries=30, step_size=10)