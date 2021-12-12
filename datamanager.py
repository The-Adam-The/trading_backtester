import pandas as pd
pd.options.mode.chained_assignment = None
from trading_strats import TradingStrats
from graphing import Graph

strats = TradingStrats()
graph = Graph()


class Datamanager():
    
    def get_signals(self, df):
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

    def back_test(self, assets):
        matrix_signals = []
        matrix_profits = []

        for i in range(len(assets)):
            try:
                frame = strats.rsi_calc(assets[i])
            except ValueError:
                print(f"Frame {i} generated a Value Error")
            else:
                buy, sell = self.get_signals(frame)
                profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values) / frame.loc[buy].Open.values
                matrix_signals.append(buy)
                matrix_profits.append(profits)

                # graph.scatter(matrix_profits, matrix_signals, frame['Adj Close'])

        all_profit = []

        for i in matrix_profits:
            for e in i:
                all_profit.append(e)

        wins = [i for i in all_profit if i > 0]
        n_wins = len(wins)
        losses = [i for i in all_profit if i <= 0]
        n_losses = len(losses)
        win_ratio = len(wins) / len(all_profit)

        return win_ratio, wins, n_wins, losses, n_losses, all_profit

