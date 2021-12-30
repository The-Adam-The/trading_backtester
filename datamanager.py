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


    #TODO: Add additional parameters amount per trade, etc...
    #TODO: Add sort mechanism that shows best performing assets

    def capital_calc(self, capital, matrix_profits, trade_fees, exposed_capital_perc=0.1):

        permitted_number_active_trades = 10
        current_exposed_capital = 0
        exposed_capital_limit = capital * exposed_capital_perc
        reserve_capital_perc = (1 - exposed_capital_perc)
        reserve_capital = capital * reserve_capital_perc

        all_trades_frames = []
        active_trades = []

        #creates a new dataframe that the capital calc can use to run through trade dates to ensure no overlapping trades
        for asset in matrix_profits:

            asset['all trades']['asset ticker'] = [asset['asset'] for x in range(len(asset['all trades']))]
            asset['all trades']['trade taken'] = ['NaN' for x in range(len(asset['all trades']))]
            all_trades_frames.append(asset['all trades'])

        all_trades_df = pd.concat(all_trades_frames)
        all_trades_df = all_trades_df.sort_values(by='buy date', ascending=True)
        all_trades_df = all_trades_df[['asset ticker', 'buy date', 'sell date', 'profit', 'trade taken']]
        all_trades_df = all_trades_df.reset_index()


        #todo: finish  the completed trades loop, it needs to pop the relevant row from the frame.
        for i in range(len(all_trades_df)):

            completed_trades = [x.index for x in active_trades if
                                all_trades_df.loc[i]['buy date'] >= x['sell date']]

            print(completed_trades)

            print(f"Amount of capital exposed: {current_exposed_capital}")
            print(f"Capital Exposure Limit as a faction: {exposed_capital_perc}")
            print(f"Capital Exposure limit value: {capital * exposed_capital_perc}")
            print(f"Number of active trades: {active_trades}")
            print(f"Number of completed trades: {completed_trades}")


            if current_exposed_capital >= (capital * exposed_capital_perc):
                print(f"Amount of capital exposure is too high. Percentage of capital exposed: {current_exposed_capital / capital * 100}. Trade aborted. ")
                all_trades_df.loc[i]['trade taken'] = 'no'

            if len(active_trades) >= permitted_number_active_trades:
                print(f"No more active trades permitted. Number of trades permitted: {permitted_number_active_trades}, Number of active trades: {len(active_trades)}")
                all_trades_df.loc[i]['trade taken'] = 'no'

            else:
                all_trades_df.loc[i]['trade taken'] = 'yes'
                active_trades.append(all_trades_df.loc[i])






        return capital

    def new_back_test(self, strat, asset_names, start_date, end_date, capital=1000, trade_fees=0):

        assets = data_pull.fetch_sp500_data_db(asset_names, start_date, end_date)

        matrix_signals = []
        matrix_profits = []
        all_profit = []


        if strat == 'rsi':

            for n in range(len(assets)):

                try:
                    frame = strats.rsi_calc(assets[n][1])


                except ValueError:
                    print(f"Frame {assets[n][0]} generated a Value Error")
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

                    profit = (frame.loc[selling_dates].Open.values -
                                                frame.loc[buying_dates].Open.values) / frame.loc[buying_dates].Open.values


                    d = {'buy date': frame.loc[buying_dates].Date.values,
                         'sell date': frame.loc[selling_dates].Date.values,
                          'profit': profit
                         }
                    profit_df = pd.DataFrame(data=d)


                    buy_dict = {'asset':assets[n][0],
                                'buying dates': buying_dates
                                }
                    profit_dict = {'asset': assets[n][0],
                                   'all trades': profit_df
                                   }
                    matrix_signals.append(buy_dict)
                    matrix_profits.append(profit_dict)

        total_wins = []
        total_losses = []

        for asset_array in (matrix_profits):

            asset_array['all trades']['winning trades'] = ["yes" if x > 0 else 'no' for x in asset_array['all trades']['profit']]
            asset_array['n winning trades'] = len(asset_array['all trades'].loc[asset_array['all trades']['winning trades'] != "no"])
            asset_array['n losing trades'] = len(asset_array['all trades'].loc[asset_array['all trades']['winning trades'] != "yes"])

            try:
                asset_array['success ratio'] = asset_array['n winning trades'] / asset_array['n losing trades']
            except ZeroDivisionError:
                print(f"ZeroDivision Error for asset: {asset_array['asset']}")
                asset_array["success ratio"] = 0

            total_wins.extend(x for x in asset_array['all trades']['profit'] if x > 0)
            total_losses.extend(x for x in asset_array['all trades']['profit'] if x < 0)



        n_total_wins = len(total_wins)
        n_total_losses = len(total_losses)

        total_win_ratio = 0

        try:
            total_win_ratio = n_total_wins / n_total_losses

        except ZeroDivisionError:
            print(f"ZeroDivisionError \nNumber of wins: {len(n_total_wins)} \nNumber of Trades: {len(all_profit)}")

        #TODO: Provide break down of profits/losses per asset

        self.capital_calc(capital, matrix_profits, trade_fees)

        return total_win_ratio, n_total_wins, n_total_losses, matrix_profits, capital





 #TODO: Continue implementing macd backtest method
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