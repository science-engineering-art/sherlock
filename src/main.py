from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.search_item import SearchItem

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
    print(query)
    return {
        "results": [
            SearchItem(title="Los pilares de la tierra", 
                snippet="Autor: Key Follet 2", score=1.2),
            SearchItem(title="Los pilares de la tierra", 
                snippet="Autor: Key Follet 3", score=20),
            SearchItem(title="Los pilares de la tierra", 
                snippet="Autor: Key Follet 1", score=1.1),
        ]
    }