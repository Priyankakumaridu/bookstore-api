from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import crud, schemas, database, auth
# trying

router = APIRouter()

@router.post("/signup", response_model=schemas.ApiResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Ensure email is lowercase for consistency
    user.email = user.email.lower()
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return {
            "status": False,
            "message": "Email already registered",
            "data": None
        }
    new_user = crud.create_user(db=db, user=user)
    return {
        "status": True,
        "message": "User created successfully",
        "data": schemas.User.model_validate(new_user)
    }

@router.post("/login", response_model=schemas.ApiResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Ensure email is lowercase for consistency
    email = form_data.username.lower()
    user = crud.get_user_by_email(db, email=email)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        return {
            "status": False,
            "message": "Incorrect email or password",
            "data": None
        }
    
    access_token_expires = timedelta(
        minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "status": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "token_type": "bearer"
        },
    }
