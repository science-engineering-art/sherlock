from models.corpus import Corpus
from models.kmeans_based_model import VectorModelKMEANS
from corpus_qrels import CranfieldQRels, VaswaniQRels, Cord19QRels

cranfield_Corpus = Corpus('cranfield')
cranfield_Vector = VectorModelKMEANS(cranfield_Corpus)
cranfield_QRels = CranfieldQRels(cranfield_Vector)
cranfield_QRels.precision_measurements(amount_docs=1400, amount_queries=225)
