from fastapi import FastAPI
from pydantic import BaseModel
from models.vector_model import VectorModel
from fastapi.middleware.cors import CORSMiddleware


class DocumentDto(BaseModel):
    doc_id: str
    title: str | None
    author: str | None
    text: str | None
    score: float | None


model = VectorModel('cranfield')

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
    for doc in model.corpus:
        if doc.doc_id == doc_id:
            return doc.text
