import ccxt
import pandas as pd

mexc = ccxt.mexc ({
    'apiKey': 'mx0DarmjbC5hmxq4Nm',
    'secret': '288c3e8215ba400f9a594d738dd3c17e',
})

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
    print(item[1])
