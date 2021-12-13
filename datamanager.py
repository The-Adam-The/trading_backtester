import pandas as pd
pd.options.mode.chained_assignment = None
from trading_strats import TradingStrats
from graphing import Graph

strats = TradingStrats()
graph = Graph()


class Datamanager():
    
    def get_rsi_signals(self, df):
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
                    buy, sell = self.get_rsi_signals(frame)
                    profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values) / frame.loc[buy].Open.values
                    matrix_signals.append(buy)
                    matrix_profits.append(profits)

        #TODO: Finish adding macd signal

        # if strat == 'macd':
        #     real_buys = [i + 1 for i in buy]
        #     real_sells = [i + 1 for i in sell]
        #
        #     buy_prices = df.Open.iloc[real_buys]
        #     sell_prices = df.Open.iloc[real_sells]
        #
        #
        #     if sell_prices.index[0] < buy_prices.index[0]:
        #         sell_prices = sell_prices.drop(sell_prices.index[0])
        #     elif buy_prices.index[-1] > sell_prices.index[-1]:
        #         buy_prices = buy_prices.drop(buy_prices.index[-1])


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

