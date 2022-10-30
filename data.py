from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Crypto

engine = create_engine('sqlite:///portfolio.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

crypto = Crypto(asset="BTC", amount="0.88", locked="0.0", exchange="abc")

session.add(crypto)
session.commit()
print(crypto.asset)