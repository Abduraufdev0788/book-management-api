from pydantic import BaseModel
from pydantic import Field

class BookBase(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: int
    rating: float = Field(ge=1, le=5, description="Rating 1 dan 5 gacha bo'lishi kerak")
    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year: int
    rating: float = Field(ge=1, le=5, description="Rating 1 dan 5 gacha bo'lishi kerak")