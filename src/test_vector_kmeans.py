from models.corpus import Corpus
from models.kmeans_based_model import VectorModelKMEANS
from corpus_qrels import CranfieldQRels, VaswaniQRels, Cord19QRels
from models.vector_model import VectorModel

cranfield_Corpus = Corpus('cranfield')
cranfield_Vector = VectorModelKMEANS(cranfield_Corpus)
cranfield_QRels = CranfieldQRels(cranfield_Vector)
cranfield_QRels.precision_measurements(amount_docs=1400, amount_queries=225)


# vaswani_Corpus = Corpus('vaswani')
# vaswani_Vector = VectorModelKMEANS(vaswani_Corpus)
# vaswani_QRels = VaswaniQRels(vaswani_Vector)
# vaswani_QRels.precision_measurements(amount_docs=11000, amount_queries= 93, step_size = 10)
