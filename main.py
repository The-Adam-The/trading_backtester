import pandas as pd
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


win_ratio, wins, n_wins, losses, n_losses, all_profit = data.back_test(scraper.pull_sp500(10))

print(f"Win Ratio: {win_ratio}")
print(f"Wins: {n_wins}")
print(f"Losses: {n_losses}")

graph.histogram(all_profit)



#TODO: Fix Scatter Graph
#TODO: Graph and calculate total profits based upon investment amount
#TODO: remove issue of overlapping trades
#TODO: Add Binance API
#TODO: Backtest strategy with Binance







