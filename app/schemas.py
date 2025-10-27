from pydantic import BaseModel

class BookBase(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: int
    rating: float