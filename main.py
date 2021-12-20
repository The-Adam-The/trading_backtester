import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from graphing import Graph
from pprint import pprint as print
from data_pull import Scraper
from trading_strats import TradingStrats
from datamanager import Datamanager
pd.options.mode.chained_assignment = None
import sqlite3

connection = sqlite3.connect('TradingData.db')
cursor = connection.cursor()



scraper = Scraper()
# strats = TradingStrats()
# data = Datamanager()
# graph = Graph()
#
#
# ASSETS = 'TSLA'
#
# #TODO: Continue implementing macd backtest method
# #TODO: Store pulled data into database
# #TODO: Graph and calculate total profits based upon investment amount
# #TODO: remove issue of overlapping trades
# #TODO: Add Binance API
# #TODO: Backtest strategy with Binance
#
#
#
#

# cursor.execute("CREATE TABLE sp500data(ticker TEXT, date TEXT, open INTEGER, high INTEGER, low INTEGER, close INTEGER, adj_close INTEGER, volume INTEGER)")




# #Select asset
ASSETS = scraper.fetch_sp500_tickers()

df = yf.download(ASSETS[:2], start='2011-01-01')
#
# df.pivot(index="ticker")

test_df = []
print(df)




        # cursor.execute("INSERT INTO sp500data VALUES(?,?,?,?,?,?,?,?)",
        #                (asset, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))

        # test_df.append(asset, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume'])

# for row in cursor:
#     print(row)


# for row in test_df:
#     print(row)

# win_ratio, wins, n_wins, losses, n_losses, all_profit = data.back_test(ASSETS, 'rsi')
#
# print(f"Win Ratio: {win_ratio}")
# print(f"Wins: {n_wins}")
# print(f"Losses: {n_losses}")








