from fastapi import FastAPI
from pydantic import BaseModel
from traitlets import FuzzyEnum
from models.corpus import Corpus
from models.vector_model import VectorModel
from models.boolean_model import BooleanModel
from models.fuzzy_model import FuzzyModel
from fastapi.middleware.cors import CORSMiddleware


class DocumentDto(BaseModel):
    doc_id: str
    title: str | None
    author: str | None
    text: str | None
    score: float | None

name_corpus = 'cranfield'
# name_corpus = 'vaswani'
# name_corpus = 'cord19/trec-covid/round1'
corpus = Corpus(name_corpus)
# model = VectorModel(corpus)
# model = BooleanModel(corpus)
model = FuzzyModel(corpus, name_corpus)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

@app.get("/search")
async def root(query: str):
    return {
        "results": [ DocumentDto(doc_id=tuple[1].doc_id, 
                    title=tuple[1].title, author=tuple[1].author, 
                    text=tuple[1].text, score=tuple[0])
                    for tuple in model.search(query)]
    }

@app.get("/document")
async def root(doc_id: str):
    for doc in model.corpus.docs:
        if doc.doc_id == doc_id:
            return doc.text
