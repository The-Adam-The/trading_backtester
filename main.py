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


start_date = "2008-09-01"
end_date = datetime_now.strftime('%Y-%m-%d')

# #TODO: Add automatic database updates
# #TODO: remove issue of overlapping trades
# #TODO: Add Binance API
# #TODO: Backtest strategy with Binance





# search_assets = ['TSLA', 'VTR', 'GM']
search_assets = ['VTR']
# search_assets = ['all_assets']




win_ratio, n_total_wins, n_total_losses, matrix_profits, capital = data.new_back_test('rsi', search_assets, start_date, end_date)

print(f"""
Aggregate Outcome:

Win Ratio: {win_ratio}
Wins: {n_total_wins}
Losses: {n_total_losses}
Capital: {capital}

""")


print("Breakdown for individual Assets")
for asset in matrix_profits:

    print(f"""
    Asset: {asset['asset']}
    Wins: {asset['n winning trades']}
    Losses: {asset['n losing trades']}
    Success Ratio: {asset['success ratio']}

    """)

