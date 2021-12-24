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
import datetime


datetime_now = datetime.datetime.now()


connection = sqlite3.connect('sp500tradedata.db')
cursor = connection.cursor()
scraper = Scraper()
# strats = TradingStrats()
data = Datamanager()
# graph = Graph()


# #TODO: Add automatic database updates
# #TODO: remove issue of overlapping trades
# #TODO: Add Binance API
# #TODO: Backtest strategy with Binance

start_date = '2009-01-01'
end_date = datetime_now.strftime('%Y-%m-%d')




# search_assets = ['TSLA', 'VTR', 'GM']
search_assets = ['VTR']
# search_assets = ['all_assets']



# asset_names = scraper.fetch_sp500_tickers()

win_ratio, wins, n_wins, losses, n_losses, all_profit, capital = data.new_back_test('rsi', search_assets, start_date, end_date)

# print(f"Win Ratio: {win_ratio}")
# print(f"Wins: {n_wins}")
# print(f"Losses: {n_losses}")
# print(f"Capital: {capital}")
#

