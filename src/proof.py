from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from traitlets import FuzzyEnum

from models.boolean_model import BooleanModel
from models.corpus import Corpus
from models.fuzzy_model import FuzzyModel
from models.vector_model import VectorModel

corpus = {
    "cranfield": Corpus('cranfield'),
    "vaswani": Corpus('vaswani'),
    "cord19/trec-covid/round1": Corpus('cord19/trec-covid/round1')
}

# model = VectorModel(corpus['cranfield'])
# model = BooleanModel(corpus['cranfield'])
model = FuzzyModel(corpus['cranfield'])

model.search('first & second | (~Leandro & ~Maricon)')