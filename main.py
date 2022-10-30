import os
from sqlite3 import connect
import sys
import pandas as pd
import ccxt  
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Crypto

engine = create_engine('sqlite:///portfolio.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()

"""
1) CREATE CONN
2) DELETE TABLE
3) INSERT DATA
4) CREATE DATAFRAME -> CSV

"""

print('CCXT Version:', ccxt.__version__)

binance = ccxt.binance ({
    'apiKey': 'MkbnBJ5mnP6GRX9bGNvgg67rCYHi1qK1DkHjfvpcanAqZzZAREcgAhszH7G36HnD',
    'secret': '3aVsdjNtmDxef2lYsevar7eRBsEu12nTvP3y1NHIqjUSvi4mC1BVPMZEh0oUc5ZK',
})
gate = ccxt.gate ({
    'apiKey': 'e35a0c3cf6943b5c11ccfca5af252e69',
    'secret': '7f111a0a173542d1832b02b4c1b9d69505e764c9a6940ddbf37c678e254d03e1',
})
kucoin = ccxt.kucoin ({
    'apiKey': '6355d709218fb800019fce56',
    'secret': '79cbbb15-cde4-42c3-9038-24946a4b0819',
    'password':'myKupass95'
})
mexc = ccxt.mexc ({
    'apiKey': 'mx0DarmjbC5hmxq4Nm',
    'secret': '288c3e8215ba400f9a594d738dd3c17e',
})


### GATE
positions = gate.fetch_balance()
data = positions['info']
df = pd.DataFrame(data)
df.columns = ["Asset", "Amount", "Locked"]
df.set_index("Asset", inplace=True)
df.to_csv('output_new.csv')
for row in data:
    crypto = Crypto(asset=row['currency'], amount=row['available'], locked=row['locked'], exchange="GATE")
    session.add(crypto)
    session.commit()
    
### BINANCE
positions = binance.fetch_balance()
data = positions['info']['balances']
df = pd.DataFrame(data)
df.columns = ["Asset", "Amount", "Locked"]
df.set_index("Asset", inplace=True)

for row in data:
    crypto = Crypto(asset=row['asset'], amount=row['free'], locked=row['locked'], exchange="BINANCE")
    
    session.add(crypto)
    session.commit()
#query = session.query(Crypto).filter_by(asset="USDT").count()

#conn = engine.connect()
#conn.execute(query)
#query = session.query(User).filter_by(name='John')

#query = session.query(Crypto).filter(Crypto.amount == "0.00000000").delete()
#conn.execute(query)


session.query(Crypto).filter(Crypto.amount=="0.00000000").delete()
session.commit()
count = session.query(Crypto).filter(Crypto.amount == "0.00000000").count()
print(count)

### KUCOIN
positions = kucoin.fetch_balance()
data = positions['info']['data']
for row in data:
    crypto = Crypto(asset=row['currency'], amount=row['balance'], locked=0, exchange="KUCOIN")
    
    session.add(crypto)
    session.commit()
    
### MEXC
symbols = []
portfolio = {}
positions = mexc.fetch_balance()
data = positions['info']['data']
for row in data:
    symbol = row
    symbols.append(row)
for symbol in symbols:
    available = data[symbol]['available']
    portfolio.update({symbol:available})
    
for item in portfolio.items():
    
    crypto = Crypto(asset=item[0], amount=item[1], locked=0, exchange="MEXC")
    
    session.add(crypto)
    session.commit()
    
import pandas as pd
df = pd.read_sql("select * from assets", conn)
print(df)
df.to_csv('portfolio.csv')   
# count = session.query(Crypto).count()

