from models import Book,Review,db_base
from sqlalchemy import and_

def getbook(isbn):
    book = db_base.query(Book).get(isbn)
    return book

def review_exists(email, isbn):
    if (db_base.query(Review).filter(and_(Review.isbn == isbn, Review.email == email)).all()):
        return True
    else:
        return False

def getSearchDetails(query, select):
    like_format = '%{}%'.format(query)
    if select == "ISBN":
        stat = db_base.query(Book).filter(Book.isbn.like(like_format)).order_by(Book.title).all()
    elif select == "Title":
        stat = db_base.query(Book).filter(Book.title.like(like_format)).order_by(Book.title).all()
    elif select == "Author":
        stat = db_base.query(Book).filter(Book.author.like(like_format)).order_by(Book.title).all()
    else:
        stat = db_base.query(Book).filter(Book.year.like(like_format)).order_by(Book.title).all()
    return stat
