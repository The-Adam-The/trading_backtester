import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from graphing import Graph
from pprint import pprint as print
from data_pull import Scraper
from trading_strats import TradingStrats
from datamanager import Datamanager
pd.options.mode.chained_assignment = None

scraper = Scraper()
strats = TradingStrats()
data = Datamanager()
graph = Graph()


# win_ratio, wins, n_wins, losses, n_losses, all_profit = data.back_test(scraper.pull_sp500(10))
#
# print(f"Win Ratio: {win_ratio}")
# print(f"Wins: {n_wins}")
# print(f"Losses: {n_losses}")
#
# graph.histogram(all_profit)



#TODO: Amend classes so they accept both MACD and RSI inputs
#TODO: Graph and calculate total profits based upon investment amount
#TODO: remove issue of overlapping trades
#TODO: Add Binance API
#TODO: Backtest strategy with Binance

df = strats.MACD('TSLA')


graph.line_plot(df.signal, df.MACD, 'signal', 'MACD')

buy, sell = [], []

for i in range(2, len(df)):
    if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:
        buy.append(i)
    elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:
        sell.append(i)

graph.macd_scatter(df.iloc[buy].index, df.iloc[buy].Close, df.iloc[sell].index, df.iloc[sell].Close, df.Close, 'TSLA Close')

real_buys = [i + 1 for i in buy]
real_sells = [i + 1 for i in sell]

buy_prices = df.Open.iloc[real_buys]
sell_prices = df.Open.iloc[real_sells]


if sell_prices.index[0] < buy_prices.index[0]:
    sell_prices = sell_prices.drop(sell_prices.index[0])
elif buy_prices.index[-1] > sell_prices.index[-1]:
    buy_prices = buy_prices.drop(buy_prices.index[-1])

profititsrel = []

for i in range(len(sell_prices)):
    profititsrel.append((sell_prices[i] - buy_prices[i])/buy_prices[i])

average_profit = sum(profititsrel)/len(profititsrel)
print(average_profit)