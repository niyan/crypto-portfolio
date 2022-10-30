import pandas as pd
import ccxt

kucoin = ccxt.kucoin ({
    'apiKey': '6355d709218fb800019fce56',
    'secret': '79cbbb15-cde4-42c3-9038-24946a4b0819',
    'password':'myKupass95'
})

positions = kucoin.fetch_balance()
data = positions['info']['data']
df = pd.DataFrame(data)
print(df)