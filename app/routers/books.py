from fastapi import APIRouter, Depends, Query, HTTPException
from app.database import Base, get_db
from ..schemas import BookBase
from sqlalchemy.orm import Session

from app.models import Book


router = APIRouter(
    prefix="/books",
   tags=["Books"]
)

@router.get('', response_model=BookBase)
async def get_books( db: Session = Depends(get_db)):
    books = db.query(Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="kitoblar yo'q")
    
    return books

@router.get('/{book_id}', response_model=BookBase)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return book
    