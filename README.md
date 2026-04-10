# Bookstore API

A simple FastAPI-based bookstore application.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Ensure PostgreSQL is running and create a database named `bookstore_db`.

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `GET /` - Welcome message
- `GET /books` - List all books
- `GET /books/{id}` - Get a specific book
- `POST /books` - Create a new book
- `PUT /books/{id}` - Update a book
- `DELETE /books/{id}` - Delete a book

## Database

Uses PostgreSQL database (`bookstore_db`). Update the connection string in `app/database.py` if needed.