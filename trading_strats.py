import pandas as pd
import yfinance as yf
from  data_pull import Scraper

asset_data = Scraper()


class TradingStrats():

    def rsi_calc(self, asset, start_date='2011-01-01'):

        df = asset

        df['MA200'] = df['Adj Close'].rolling(
            window=200).mean()  # Get the rolling mean for the adjusted closing price from the last 200 days
        df['price change'] = df['Adj Close'].pct_change()  # Get daily relative returns
        df['Upmove'] = df['price change'].apply(lambda x: max(x, 0))
        df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)  # Get price changes
        df['avg Up'] = df['Upmove'].ewm(
            span=19).mean()  # Find average upmove by using 19 days exponential moving window
        df['avg Down'] = df['Downmove'].ewm(
            span=19).mean()  # Find average downmove by using 19 days exponential moving window
        df = df.dropna()  # drop missing values
        df['RS'] = df['avg Up'] / df['avg Down']  # calculate relative strength
        df['RSI'] = df['RS'].apply(lambda x: 100 - (100 / (x + 1)))  # calculate relative strength index
        df.loc[(df['Adj Close'] > df['MA200']) & (df[
                                                      'RSI'] < 30), 'Buy'] = 'Yes'  # if adj closing price is higher than the MA200 and RSI is less than 30: buy
        df.loc[(df['Adj Close'] < df['MA200']) | (df[
                                                      'RSI'] > 30), 'Buy'] = 'No'  # if adj closing price is lower than the MA200 and the RSI is higher than: do not buy
        return df

    def macd_calc(self, asset, start_date='2010-01-01'):
        df = yf.download(asset, start=start_date)
        df['EMA12'] = df.Close.ewm(span=12).mean()
        df['EMA26'] = df.Close.ewm(span=26).mean()
        df['MACD'] = df.EMA12 - df.EMA26
        df['signal'] = df.MACD.ewm(span=9).mean()
        print("Indicators Added")

        return df