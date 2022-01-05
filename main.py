import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from graphing import Graph
from pprint import pprint as print
from data_pull import DataPull
from trading_strats import TradingStrats
from datamanager import DataManager
pd.options.mode.chained_assignment = None
import sqlite3
import datetime


datetime_now = datetime.datetime.now()
connection = sqlite3.connect('sp500tradedata.db')
cursor = connection.cursor()
data_pull = DataPull()
data = DataManager()
# graph = Graph()


START_DATE = "2008-09-01"
END_DATE = datetime_now.strftime('%Y-%m-%d')
LIQUIDITY = 1000

# ASSETS = ['TSLA', 'VTR', 'GM']
# ASSETS = ['VTR']
ASSETS = ['all_assets']


#functions
def back_test_strategy(strat: str, assets, capital, start_date, end_date):
    '''Back Test Function'''

    assets_db = data_pull.fetch_sp500_data_db(assets, start_date, end_date)
    matrix_signals, matrix_profits = data.rsi_back_test(assets_db)
    total_portfolio_performance, matrix_profits = data.back_test_evaluation(matrix_profits)
    all_trades_df = data.create_dataframe(matrix_profits)
    all_trades_df = data.capital_calculation(capital, all_trades_df, buy_fees=0, sell_fees=0, exposed_capital_perc=0.5,
                                             permitted_number_active_trades=40)
    return all_trades_df, total_portfolio_performance, matrix_profits


all_trades_df, total_portfolio_performance, matrix_profits = back_test_strategy('rsi', ASSETS, LIQUIDITY, START_DATE, END_DATE)

print(total_portfolio_performance)
# print(all_trades_df.to_string())



# print("Breakdown for individual Assets")
# for asset in matrix_profits:
#
#     print(f"""
#     Asset: {asset['asset']}
#     Wins: {asset['n winning trades']}
#     Losses: {asset['n losing trades']}
#     Success Ratio: {asset['success ratio']}
#
#     """)

