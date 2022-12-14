from fastapi import FastAPI
from pydantic import BaseModel
from models.corpus import CorpusWithOnlyNouns
from models.vector_model import VectorModel
from fastapi.middleware.cors import CORSMiddleware

class DocumentDto(BaseModel):
    doc_id: str
    title: str
    author: str
    text: str
    score: float

corpus = {
    "cranfield": CorpusWithOnlyNouns('cranfield'),
    "vaswani": CorpusWithOnlyNouns('vaswani'),
    "cord19/trec-covid/round1": CorpusWithOnlyNouns('cord19/trec-covid/round1')
}

model = VectorModel(corpus['vaswani'])

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
async def root(dataset: str, query: str):
    result = []    

    for tuple in model.search(query):
        if abs(tuple[0]) < 1e-16: break
        doc = corpus['vaswani'].get_doc(tuple[1])
        result.append(DocumentDto(doc_id=doc['doc_id'], 
            title=doc['title'], author=doc['author'], 
            text=doc['text'], score=tuple[0]))

    return { "results": result }
