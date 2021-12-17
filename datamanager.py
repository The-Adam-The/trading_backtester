import pandas as pd
pd.options.mode.chained_assignment = None
from trading_strats import TradingStrats
from graphing import Graph

strats = TradingStrats()
graph = Graph()


class Datamanager():

    def get_macd_signals(self, df):
        buying_dates, selling_dates = [], []

        for i in range(2, len(df)):
            if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:
                buying_dates.append(i)
            elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:
                selling_dates.append(i)



    def back_test(self, assets, strat):

        matrix_signals = []
        matrix_profits = []

        if strat == 'rsi':

            for i in range(len(assets)):
                try:
                    frame = strats.rsi_calc(assets[i])
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

        #TODO: Finish adding macd signal

        if strat == 'macd':

            buying_dates, selling_dates = [], []

            for i in range(len(assets)):
                frame = strats.macd_calc(assets[i])

                for i in range(2, len(assets)):
                    if frame.MACD.iloc[i] > frame.signal.iloc[i] and frame.MACD.iloc[i - 1] < frame.signal.iloc[i - 1]:
                        buying_dates.append(i)
                    elif frame.MACD.iloc[i] < frame.signal.iloc[i] and frame.MACD.iloc[i - 1] > frame.signal.iloc[i - 1]:
                        selling_dates.append(i)

                real_buys = [i + 1 for i in buying_dates]
                real_sells = [i + 1 for i in selling_dates]

                buy_prices = frame.Open.iloc[real_buys]
                sell_prices = frame.Open.iloc[real_sells]


                if sell_prices.index[0] < buy_prices.index[0]:
                    sell_prices = sell_prices.drop(sell_prices.index[0])
                elif buy_prices.index[-1] > sell_prices.index[-1]:
                    buy_prices = buy_prices.drop(buy_prices.index[-1])

                matrix_signals.append(buying_dates)

                for i in range(len(sell_prices)):

                    matrix_profits.append((sell_prices[i] - buy_prices[i])/buy_prices[i])

                # average_profit = sum(matrix_profits)/len(matrix_profits)
                # print(average_profit)


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

