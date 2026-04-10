from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from jose import JWTError, jwt
from app import crud, models, schemas, database, auth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/", response_model=schemas.ApiResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Check if a book with the same title already exists for a DIFFERENT author
    existing_title_book = crud.get_book_by_title_insensitive(db, book.title)
    if existing_title_book:
        if existing_title_book.author != book.author:
            return {
                "status": False,
                "message": f"The title '{book.title}' is already used by author '{existing_title_book.author}'. A different author cannot use this title.",
                "data": None
            }
    
    # Check if the category is already used by a DIFFERENT author
    existing_category_book = crud.get_book_by_category(db, book.category)
    if existing_category_book:
        if existing_category_book.author != book.author:
            return {
                "status": False,
                "message": f"The category '{book.category}' is already claimed by author '{existing_category_book.author}'. A different author cannot use this category.",
                "data": None
            }

    try:
        new_book = crud.create_book(db=db, book=book)
        return {
            "status": True,
            "message": "Book created successfully",
            "data": schemas.Book.model_validate(new_book)
        }
    except IntegrityError:
        db.rollback()
        return {
            "status": False,
            "message": "Book with the same title, category, and author already exists",
            "data": None
        }

@router.get("/", response_model=schemas.ApiResponse)
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return {
        "status": True,
        "message": "Books retrieved successfully",
        "data": [schemas.Book.model_validate(book) for book in books]
    }

@router.get("/{book_id}", response_model=schemas.ApiResponse)
def read_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        return {
            "status": False,
            "message": "Book not found",
            "data": None
        }
    return {
        "status": True,
        "message": "Book retrieved successfully",
        "data": schemas.Book.model_validate(db_book)
    }

@router.put("/{book_id}", response_model=schemas.ApiResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    try:
        db_book = crud.update_book(db, book_id=book_id, book=book)
        if db_book is None:
            return {
                "status": False,
                "message": "Book not found",
                "data": None
            }
        return {
            "status": True,
            "message": "Book updated successfully",
            "data": schemas.Book.model_validate(db_book)
        }
    except IntegrityError:
        db.rollback()
        return {
            "status": False,
            "message": "Update failed: Book with the same title, category, and author already exists",
            "data": None
        }

@router.delete("/{book_id}", response_model=schemas.ApiResponse)
def delete_book(book_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        return {
            "status": False,
            "message": "Book not found",
            "data": None
        }
    return {
        "status": True,
        "message": "Book deleted successfully",
        "data": None
    }