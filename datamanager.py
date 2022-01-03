import pandas as pd
import numpy as np
from trading_strats import TradingStrats
from graphing import Graph
from data_pull import Scraper
import sqlite3

pd.options.mode.chained_assignment = None

connection = sqlite3.connect('TradingData.db')
cursor = connection.cursor()
strats = TradingStrats()
graph = Graph()
data_pull = Scraper()


class DataManager:
    #TODO: Add additional parameters amount per trade, etc...
    #TODO: Add sort mechanism that shows best performing assets

    def capital_calculation(self, total_liquidity, matrix_profits, buy_fees=0, sell_fees=0, exposed_capital_perc=0.1,
                            permitted_number_active_trades=10):

        all_trades_frames = []
        active_trade_indexes = []
        completed_trade_index = []

        #creates a new dataframe that the capital calc can use to run through trade dates to ensure no overlapping trades
        for asset in matrix_profits:

            asset['all trades']['asset ticker'] = [asset['asset'] for _ in range(len(asset['all trades']))]
            asset['all trades']['trade active'] = [None for _ in range(len(asset['all trades']))]
            asset['all trades']['amount invested'] = [np.nan for _ in range(len(asset['all trades']))]
            asset['all trades']['amount disinvested'] = [np.nan for _ in range(len(asset['all trades']))]
            asset['all trades']['profit($)'] = [np.nan for _ in range(len(asset['all trades']))]
            asset['all trades']['profit($)'] = [np.nan for _ in range(len(asset['all trades']))]
            all_trades_frames.append(asset['all trades'])

        all_trades_df = pd.concat(all_trades_frames)
        all_trades_df = all_trades_df.sort_values(by='buy date', ascending=True)
        all_trades_df = all_trades_df.reset_index(drop='index')

        # initial variables
        value_equities = 0
        exposed_capital_limit = total_liquidity * exposed_capital_perc
        reserve_capital_perc = (1 - exposed_capital_perc)
        reserve_capital = total_liquidity * reserve_capital_perc
        value_per_trade = exposed_capital_limit / permitted_number_active_trades

        print(f"total_capital before transactions: {total_liquidity}")

        for i in range(len(all_trades_df)):

            for idx, active_trade_index in enumerate(active_trade_indexes):
                try:
                    if all_trades_df.loc[i]['buy date'] >= all_trades_df.loc[active_trade_index]['sell date']:
                        print(f"Most recent trade opportunity: {all_trades_df.loc[i]['buy date']} is past the sell date of active_trade(s) {all_trades_df.loc[active_trade_index]['sell date']}. Trade removed from active_list")
                        all_trades_df.at[active_trade_index, 'amount disinvested'] = (all_trades_df.loc[active_trade_index]['amount invested'] + (all_trades_df.loc[active_trade_index]['profit'] * all_trades_df.loc[active_trade_index]['amount invested'])) - sell_fees
                        all_trades_df.at[active_trade_index, 'trade active'] = False

                        value_equities -= all_trades_df.loc[active_trade_index]['amount invested']
                        total_liquidity += all_trades_df.loc[active_trade_index]['amount disinvested']
                        all_trades_df.at[active_trade_index, 'profit($)'] = all_trades_df.loc[active_trade_index, 'amount disinvested'] - (all_trades_df.loc[active_trade_index, 'amount invested'])
                        all_trades_df.at[active_trade_index, 'portfolio value($)'] = total_liquidity + value_equities
                        exposed_capital_limit = (total_liquidity + value_equities) * exposed_capital_perc
                        value_per_trade = exposed_capital_limit / permitted_number_active_trades
                        completed_trade_index.append(active_trade_indexes.pop(idx))

                except IndexError:
                    print("index error for active_trade_index")

            if value_equities >= (total_liquidity * exposed_capital_perc):
                print(f"Amount of capital exposure is too high. Percentage of capital exposed: {value_equities / total_liquidity * 100}. Trade aborted.")
                all_trades_df.loc[i]['trade active'] = False

            if len(active_trade_indexes) >= permitted_number_active_trades:
                print(f"No more active trades permitted. Number of trades permitted: {permitted_number_active_trades}, Number of active trades: {len(active_trade_indexes)}")
                all_trades_df.loc[i]['trade active'] = False

            else:
                all_trades_df.at[i, 'trade active'] = True
                all_trades_df.at[i, 'amount invested'] = value_per_trade - buy_fees
                print(f"Trade Performed. Amount invested: {all_trades_df.loc[i]['amount invested']}")
                value_equities += all_trades_df.loc[i]['amount invested']
                print(f"current_exposed_capital buy: {value_equities}")
                total_liquidity -= all_trades_df.loc[i]['amount invested']
                print(f"reserve_capital buy: {reserve_capital}")
                active_trade_indexes.append(i)



        print(f"Amount of capital exposed: {value_equities}")
        print(f"Capital Exposure Limit as a fraction: {exposed_capital_perc}")
        print(f"Capital Exposure limit value: {total_liquidity * exposed_capital_perc}")
        print(f"Number of outstanding trades: {len(active_trade_indexes)}")

        print(all_trades_df.to_string())
        return all_trades_df

    def back_test(self, strat, asset_names, start_date, end_date, capital=1000):

        assets = data_pull.fetch_sp500_data_db(asset_names, start_date, end_date)

        if strat == 'rsi':

            matrix_signals = []
            matrix_profits = []

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

                    d = {
                            'buy date': frame.loc[buying_dates].Date.values,
                            'sell date': frame.loc[selling_dates].Date.values,
                            'profit': profit
                         }
                    profit_df = pd.DataFrame(data=d)

                    buy_dict = {
                            'asset': assets[n][0],
                            'buying dates': buying_dates
                                }
                    profit_dict = {
                            'asset': assets[n][0],
                            'all trades': profit_df
                                   }
                    matrix_signals.append(buy_dict)
                    matrix_profits.append(profit_dict)

        total_wins = []
        total_losses = []

        for asset_array in matrix_profits:

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
            print(f"ZeroDivisionError \nNumber of wins: {n_total_wins} \nNumber of Trades: {n_total_wins + n_total_losses}")

        #TODO: Provide break down of profits/losses per asset

        self.capital_calculation(capital, matrix_profits)

        return total_win_ratio, n_total_wins, n_total_losses, matrix_profits, capital
