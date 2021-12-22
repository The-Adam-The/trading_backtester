import pandas as pd
pd.options.mode.chained_assignment = None
from trading_strats import TradingStrats
from graphing import Graph
from  data_pull import Scraper
import sqlite3

connection = sqlite3.connect('TradingData.db')
cursor = connection.cursor()
strats = TradingStrats()
graph = Graph()
data_pull = Scraper()




class Datamanager():

    def get_macd_signals(self, df):
        buying_dates, selling_dates = [], []

        for i in range(2, len(df)):
            if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:
                buying_dates.append(i)
            elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:
                selling_dates.append(i)



    def new_back_test(self, strat, asset_names, start_date='2010-01-01'):



        assets = data_pull.fetch_sp500_data_db(asset_names,start_date)



        matrix_signals = []
        matrix_profits = []

        if strat == 'rsi':

            for i in range(len(assets)):
                try:
                    frame = strats.rsi_calc(assets[i][1])
                except ValueError:
                    print(f"Frame {i} generated a Value Error")
                else:
                    buying_dates = []
                    selling_dates = []

                    for i in range(len(frame) - 11):
                        if "Yes" in frame['Buy'].iloc[i]:
                            buying_dates.append(frame.iloc[i + 1].name)
                            for j in range(1, 11):
                                if frame['RSI'].iloc[i + j] > 40:
                                    selling_dates.append(frame.iloc[i + j + 1].name)
                                    break
                                elif j == 10:
                                    selling_dates.append(frame.iloc[i + j + 1].name)

                    profits = (frame.loc[selling_dates].Open.values - frame.loc[buying_dates].Open.values) / frame.loc[buying_dates].Open.values
                    matrix_signals.append(buying_dates)
                    matrix_profits.append(profits)


        all_profit = []

        for i in matrix_profits:
            if strat == 'rsi':
                for e in i:
                    all_profit.append(e)
            else:
                all_profit.append(i)

        wins = [i for i in all_profit if i > 0]
        n_wins = len(wins)
        losses = [i for i in all_profit if i <= 0]
        n_losses = len(losses)
        win_ratio = len(wins) / len(all_profit)

        return win_ratio, wins, n_wins, losses, n_losses, all_profit






#TODO: Finish adding macd signal
 # if strat == 'macd':
        #
        #     buying_dates, selling_dates = [], []
        #
        #     for i in range(len(assets)):
        #         frame = strats.macd_calc(assets[i])
        #
        #         for i in range(2, len(assets)):
        #             if frame.MACD.iloc[i] > frame.signal.iloc[i] and frame.MACD.iloc[i - 1] < frame.signal.iloc[i - 1]:
        #                 buying_dates.append(i)
        #             elif frame.MACD.iloc[i] < frame.signal.iloc[i] and frame.MACD.iloc[i - 1] > frame.signal.iloc[i - 1]:
        #                 selling_dates.append(i)
        #
        #         real_buys = [i + 1 for i in buying_dates]
        #         real_sells = [i + 1 for i in selling_dates]
        #
        #         matrix_signals.append(buying_dates)
        #
        #         buy_prices = frame.Open.iloc[real_buys]
        #         sell_prices = frame.Open.iloc[real_sells]


                # if sell_prices.index[0] < buy_prices.index[0]:
                #     sell_prices = sell_prices.drop(sell_prices.index[0])
                # elif buy_prices.index[-1] > sell_prices.index[-1]:
                #     buy_prices = buy_prices.drop(buy_prices.index[-1])
                #
                #
                # for i in range(len(sell_prices)):
                #     try:
                #         matrix_profits.append((sell_prices[i] - buy_prices[i])/buy_prices[i])
                #     except IndexError:
                #         print("Index Error")
                #
                # print(matrix_profits)

                # average_profit = sum(matrix_profits)/len(matrix_profits)
                # print(average_profit)




# graph.line_plot(df.signal, df.MACD, 'signal', 'MACD')

# buy, sell = [], []
#
# for i in range(2, len(df)):
#     if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:
#         buy.append(i)
#     elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:
#         sell.append(i)
#
# graph.macd_scatter(df.iloc[buy].index, df.iloc[buy].Close, df.iloc[sell].index, df.iloc[sell].Close, df.Close, 'TSLA Close')
#
# real_buys = [i + 1 for i in buy]
# real_sells = [i + 1 for i in sell]
#
# buy_prices = df.Open.iloc[real_buys]
# sell_prices = df.Open.iloc[real_sells]
#
#
# if sell_prices.index[0] < buy_prices.index[0]:
#     sell_prices = sell_prices.drop(sell_prices.index[0])
# elif buy_prices.index[-1] > sell_prices.index[-1]:
#     buy_prices = buy_prices.drop(buy_prices.index[-1])
#
# profititsrel = []
#
# for i in range(len(sell_prices)):
#     profititsrel.append((sell_prices[i] - buy_prices[i])/buy_prices[i])
#
# average_profit = sum(profititsrel)/len(profititsrel)
# print(average_profit)
#
#
#
# # graph.histogram(all_profit)