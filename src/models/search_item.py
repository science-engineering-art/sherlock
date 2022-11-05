from pydantic import BaseModel


class SearchItem(BaseModel):
    title: str
    snippet: str
    score: float or 0