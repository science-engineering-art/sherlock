from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchItem(BaseModel):
    title: str
    snippet: str
    score: float

@app.get("/search")
async def root(query: str):
    print(query)
    return {
        "results": [
            SearchItem(title="Los pilares de la tierra", snippet="Autor", score=3),
            SearchItem(title="Los pilares de la tierra", snippet="Autor", score=3),
            SearchItem(title="Los pilares de la tierra", snippet="Autor", score=3)
        ]
    }