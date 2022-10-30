from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# https://leportella.com/sqlalchemy-tutorial/

engine = create_engine('sqlite:///portfolio.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

conn = engine.connect()

query = "DROP table IF EXISTS assets"

conn.execute(query)

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class Crypto(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    asset = Column(String)
    amount = Column(String)
    locked = Column(String)
    exchange = Column(String)
    
    def __repr__(self):
        return f'Crypto {self.name}'

Base.metadata.create_all(engine)

