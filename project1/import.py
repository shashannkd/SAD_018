import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Book

engine = create_engine(os.getenv("DATABASE_URL"))
database = scoped_session(sessionmaker(bind=engine))
db = database()


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    i = 0

    for isbn, title, author, year in reader:
        if i != 0:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                       {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added {isbn} ,{title} , {author},{year} row")
        i = i+1
    db.commit()


db.close()

if __name__ == '__main__':
    main()
