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


dfs = []
for symbol, team in zip(stonks, teams):
    my_share = yf.Ticker(symbol)
    df = my_share.history(start='2020-08-31', interval='1m')
    df.fillna(method='ffill')
    dfs.append(df)


master_df = dfs[0]
master_df[f"{teams[0]}-{stonks[0]}"] = master_df['Close']/opens[0] - 1
for i, df in enumerate(dfs):
    if i == 0:
        continue
    my_df = dfs[i][:len(master_df)]
    team_name = f"{teams[i]}-{stonks[i]}"
    master_df[team_name] = my_df['Close']/opens[i] - 1

master_df = dfs[0]
master_df[f"{teams[0]}-{stonks[0]}"] = master_df['Close']/opens[0] - 1
for i, df in enumerate(dfs):
    if i == 0:
        continue
    my_df = dfs[i][:len(master_df)]
    team_name = f"{teams[i]}-{stonks[i]}"
    master_df[team_name] = my_df['Close']/opens[i] - 1

master_df = master_df.fillna(method='ffill')
team_names = []
for i in range(len(teams)):
    name = f"{teams[i]}-{stonks[i]}"
    team_names.append(name)
master_df['Date'] = master_df.index

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(30,10))
ax1.grid()
ax2.grid()

min_y = 0
max_y = 0
for i, tn in enumerate(team_names[:7]):
    marker_id = i
    if marker_id > 11:
        marker_id = 0
    min_y = min(min_y, min(master_df[tn]))
    max_y = max(max_y, max(master_df[tn]))
    ax1.plot(master_df['Date'], master_df[tn], marker=marker_id)
ax1.legend(team_names[:7], loc='upper center', ncol=len(team_names)//2)
for i, tn in enumerate(team_names[7:]):
    marker_id = i
    if marker_id > 11:
        marker_id = 0
    min_y = min(min_y, min(master_df[tn]))
    max_y = max(max_y, max(master_df[tn]))
    ax2.plot(master_df['Date'], master_df[tn], marker=marker_id)
ax1.set_ylim([min_y, max_y])
ax2.set_ylim([min_y, max_y])
ax2.legend(team_names[7:], loc='upper center', ncol=len(team_names)//2)
fig.patch.set_facecolor('white')
plt.savefig('stonks.png')
