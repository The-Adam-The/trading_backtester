import pandas as pd
import yfinance as yf
from pprint import pprint as print

import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

#pull tickers from the S&P 500 Wikipedia page
tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]

tickers = tickers.Symbol.to_list()



# '.' causes errors
tickers = [i.replace('.', '-') for i in tickers]


#VNT and WRK are problem cases
# print(tickers.pop(474))
# print(tickers.pop(489))

def rsi_calc(asset):
    df = yf.download(asset, start='2011-01-01')

    df['MA200'] = df['Adj Close'].rolling(window=200).mean() #Get the rolling mean for the adjusted closing price from the last 200 days

    df['price change'] = df['Adj Close'].pct_change() #Get daily relative returns

    df['Upmove'] = df['price change'].apply(lambda x: x if x > 0 else 0)

    df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0) #Get price changes

    df['avg Up'] = df['Upmove'].ewm(span=19).mean() #Find average upmove by using 19 days exponential moving window

    df['avg Down'] = df['Downmove'].ewm(span=19).mean() #Find average downmove by using 19 days exponential moving window

    df = df.dropna() #drop missing values

    df['RS'] = df['avg Up']/df['avg Down'] #calculate relative strength

    df['RSI'] = df['RS'].apply(lambda x: 100 - (100/(x+1))) #calculate relative strength index

    df.loc[(df['Adj Close'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = 'Yes' # if adj closing price is higher than the MA200 and RSI is less than 30: buy

    df.loc[(df['Adj Close'] < df['MA200']) | (df['RSI'] > 30), 'Buy'] = 'No' # if adj closing price is lower than the MA200 and the RSI is higher than: do not buy


    return df


def getSignals(df):
    buying_dates = []
    selling_dates = []

    for i in range(len(df) - 11):
        if "Yes" in df['Buy'].iloc[i]:
            buying_dates.append(df.iloc[i+1].name)
            for j in range(1, 11):
                if df['RSI'].iloc[i + j] > 40:
                    selling_dates.append(df.iloc[i+j+1].name)
                    break
                elif j == 10:
                    selling_dates.append(df.iloc[i+j+1].name)

    return buying_dates, selling_dates





#Test code

# frame = rsi_calc(tickers[0])
# buy, sell = getSignals(frame)

#Without Averaged values
# profits = frame.loc[sell].Open.values - frame.loc[buy].Open.values
# print(profits)

#With Averaged Values
# averaged_profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values

# wins = [i for i in averaged_profits if i > 0]
#
# win_rate = len(wins)/len(averaged_profits)


# plt.figure(figsize=(12, 5))
# plt.scatter(frame.loc[buy].index, frame.loc[buy]['Adj Close'], marker='^', c='g')
# plt.plot(frame['Adj Close'], alpha=0.7)
# plt.show()

#Backtest strategy

matrix_signals = []
matrix_profits = []


for i in range(len(tickers)):
    try:
        frame = rsi_calc(tickers[i])
    except ValueError:
        print(f"Frame {i} generated a Value Error")
        pass
    else:
        buy, sell = getSignals(frame)
        Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
        matrix_signals.append(buy)
        matrix_profits.append(Profits)



all_profit = []

for i in matrix_profits:
    for e in i:
        all_profit.append(e)


wins = [i for i in all_profit if i > 0]
win_ratio = len(wins)/len(all_profit)

print(f"Win Ratio: {win_ratio}")

plt.hist(all_profit, bins=100)
plt.show()

#TODO Add Binance API
#TODO Backtest strategy with Binance