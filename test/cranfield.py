import ir_datasets
# from src.models.vector_model import VectorModel

# corpus = CorpusWithOnlyNouns('cranfield')
# model = VectorModel(corpus)

dataset = ir_datasets.load('cranfield')

for qrel in dataset.qrels_iter():
    print(qrel.query_id)

