from fastapi import FastAPI
from pydantic import BaseModel
from models.vector_model import VectorModel
from fastapi.middleware.cors import CORSMiddleware


class DocumentDto(BaseModel):
    path: str
    score: float | None


model = VectorModel('/home/leandro/study/3rd-year/projects' +
    '/information-retrieval-systems/corpus/moogle')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def root(query: str):

    return {
        "results": [ DocumentDto(path=tuple[1].path, score=tuple[0])
                    for tuple in model.search(query) ]
    }

@app.get("/document")
async def root(path: str):
    return open(path, 'r').read()