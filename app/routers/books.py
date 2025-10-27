from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import BookBase, BookCreate
from app.models import Book

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get('', response_model=list[BookBase])
async def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="Kitoblar yo'q")
    return books


@router.get('/{book_id}', response_model=BookBase)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return book

@router.post('', response_model=BookCreate)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put('/{book_id}', response_model=BookBase)
async def update_book(book_id: int, book: BookBase, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    db_book.title = book.title
    db_book.author = book.author
    db_book.genre = book.genre
    db_book.year = book.year
    db_book.rating = book.rating
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete('/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    db.delete(db_book)
    db.commit()
    return {"detail": "Kitob o'chirildi"}

@router.get("/search", response_model=list[BookBase])
async def search_books(query: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(
        or_(
            Book.title.ilike(f"%{query}%"),
            Book.author.ilike(f"%{query}%")
        )
    ).all()

    if not books:
        raise HTTPException(status_code=404, detail="Hech qanday kitob topilmadi")
    return books



