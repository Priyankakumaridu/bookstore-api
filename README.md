# Bookstore API Documentation

## Overview
This is a RESTful API for managing a bookstore application built using FastAPI. The API enables users to perform various CRUD operations on books, authors, and categories.

## Technology Stack
The application is built with the following technologies:
- **FastAPI** - A modern web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **PostgreSQL** - A powerful, open source object-relational database system.
- **SQLAlchemy** - The Python SQL Toolkit and Object-Relational Mapping (ORM) system.
- **Alembic** - A lightweight database migration tool for use with SQLAlchemy.
- **Uvicorn** - A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.

## API Endpoints
- **GET /books** - Retrieve a list of books.
- **POST /books** - Create a new book.
- **GET /books/{book_id}** - Retrieve details of a specific book.
- **PUT /books/{book_id}** - Update a specific book.
- **DELETE /books/{book_id}** - Delete a specific book.

## Database Models
- **Book** - Represents a book in the bookstore.
- **Author** - Represents an author associated with books.
- **Category** - Represents categories that books can belong to.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Priyankakumaridu/bookstore-api.git
   cd bookstore-api
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   alembic upgrade head
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

## Usage
After starting the server, you can interact with the API using tools like Postman or CURL. Ensure that PostgreSQL is running and the database is named as specified in the configuration file.

## License
This project is licensed under the MIT License.