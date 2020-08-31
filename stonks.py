import yfinance as yf
import pandas as pd


def get_open_price(my_share, symbol):
    if symbol == 'TSLA':
        return 473.26
    hist = my_share.history(period='5d')
    hist['Date'] = hist.index
    df = hist[hist['Date'] == '2020-08-31']
    open_price = df['Open'].values[0]
    return open_price
def get_now_price(my_share):
    now_table = my_share.history(period='1d', interval='1m')
    now_price = now_table['Open'].values[-1]
    return now_price

stonks = ['CP', 'WORK', 'GRVY', 'CRWD', 'RKT', 'SKYW', 'CWH', 'MRNA', 'MU', 'FIZZ', 'TSLA', 'ALK', 'EDSA', 'BB']
teams = ['Ethan', 'Jelly', 'Gravy', 'Lutes', 'Brian', 'Susan', 'Erin', 'Ana', 'Jarel', 'Erik', 'Daniel', 'Hayne', 'Ivan', 'Kalish']
table = []
for symbol, team in zip(stonks, teams):
    my_share = yf.Ticker(symbol)
    row = [team, symbol, get_open_price(my_share, symbol), get_now_price(my_share)]
    row.append(row[-1]/row[-2] - 1)
    table.append(row)


df = pd.DataFrame(table)
df.columns = ['Team', 'Stonk', 'Open', 'Now', 'Gainz']
df = df.sort_values('Gainz', ascending=False)
df['Gainz'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['Gainz']], index = df.index)
df.index = list(range(1, len(df)+1))
df.to_html('stonks.html')
