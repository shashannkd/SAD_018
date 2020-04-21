import os
import csv
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

db_base = declarative_base()


class User(db_base):
    __tablename__ = "users"
    email = Column(String(30), primary_key=True)
    name = Column(String(30), nullable=False)
    pswd = Column(String(100), nullable=False)
    dob = Column(String(15),nullable = False)
    timestamp = Column(DateTime(timezone=True), nullable=False)


engine = create_engine(os.getenv("DATABASE_URL"))
db_base.metadata.create_all(engine)
