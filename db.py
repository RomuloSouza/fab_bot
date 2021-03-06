#!/usr/bin/env python3.6.7

from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite3', echo=True)
SESSION = sessionmaker(bind=engine)
SESSION = SESSION()

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    chat = Column(Integer)
    name = Column(String)
    price = Column(String)
    quantity = Column(Integer)

    def __repr__(self):
        return "<Cart(id={}, chat={}, name='{}', price='{}')>".format(
            self.id, self.chat, self.name, self.price
        )

Base.metadata.create_all(engine)
