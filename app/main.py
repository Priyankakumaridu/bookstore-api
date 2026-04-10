from fastapi import FastAPI
from app.routes.book import router as book_router
from app.routes.auth import router as auth_router
from app.database import engine
from app import models

# Note: We keep this for now, but Alembic will manage migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API", version="1.0.0")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(book_router, prefix="/books", tags=["books"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bookstore API"}