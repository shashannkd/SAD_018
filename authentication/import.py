import os
import csv
from models import Book
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))
db = db_session()


with open("books.csv", 'r') as books_file:
    books = csv.reader(books_file, delimiter=",")
    header = next(books)
    if header != None:
        for ISBN, title, author, year in books:
            book = Book(isbn=ISBN, title=title, author=author, year=year)
            print(book.title)
            db.add(book)
db.commit()
db.close()
