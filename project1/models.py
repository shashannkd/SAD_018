import os
import csv
from sqlalchemy import Column, String, Integer, DateTime, create_engine, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

db_base = declarative_base()


class Book(db_base):
    __tablename__ = "books"
    isbn = Column(String(30), primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    year = Column(String(10), nullable=False)


class User(db_base):
    __tablename__ = "users"
    email = Column(String(30), primary_key=True)
    name = Column(String(30), nullable=False)
    pswd = Column(String(100), nullable=False)
    dob = Column(String(15), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

class Review(db_base):
    __tablename__ = "user_reviews"
    isbn = Column(String(30), ForeignKey('books.isbn'))
    email = Column(String(30), ForeignKey('users.email'))
    rating = Column(Integer, nullable=False, default = 0)
    review = Column(String(150), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("isbn", "email"),)

engine = create_engine(os.getenv("DATABASE_URL"))
db_base.metadata.create_all(engine)
