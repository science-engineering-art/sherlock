from core.models.common.corpus import Corpus
from core.models.boolean_model import BooleanModel
from corpus_qrels import CranfieldQRels, VaswaniQRels, Cord19QRels

# cranfield_Corpus = Corpus('cranfield')
# cranfield_Vector = BooleanModel(cranfield_Corpus)
# cranfield_QRels = CranfieldQRels(cranfield_Vector)
# cranfield_QRels.precision_measurements(amount_docs=1400, amount_queries=225)

cranfield_Corpus = Corpus('cranfield')
cranfield_Vector = BooleanModel(cranfield_Corpus)
cranfield_QRels = CranfieldQRels(cranfield_Vector)
cranfield_QRels.no_ranked_precision_measurements(
    amount_queries=225, step_size=1)

# vaswani_Corpus = Corpus('vaswani')
# vaswani_Vector = BooleanModel(vaswani_Corpus)
# vaswani_QRels = VaswaniQRels(vaswani_Vector)
# vaswani_QRels.precision_measurements(amount_docs=11000, amount_queries=93, step_size = 20)

# vaswani_Corpus = Corpus('vaswani')
# vaswani_Vector = BooleanModel(vaswani_Corpus)
# vaswani_QRels = VaswaniQRels(vaswani_Vector)
# vaswani_QRels.no_ranked_precision_measurements(amount_queries=93, step_size=20)

# cord19_Corpus = Corpus('cord19/trec-covid/round1')
# cord19_Vector = BooleanModel(cord19_Corpus)
# cord19_QRels = Cord19QRels(cord19_Vector)
# cord19_QRels.precision_measurements(amount_docs=51000, amount_queries=30)
