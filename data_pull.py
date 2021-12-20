import pandas as pd
pd.options.mode.chained_assignment = None
import sqlite3


connection = sqlite3.connect('TradingData.db')
cursor = connection.cursor()

# cursor.execute('CREATE TABLE sp500tickers(ticker TEXT)')
# connection.commit()

class Scraper:

    def pull_sp500(self, number_sp=500):
        tickers = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0][: number_sp - 1]

        tickers = tickers.Symbol.to_list()
        # '.' causes errors
        tickers = [i.replace('.', '-') for i in tickers]

        for ticker in tickers:
            cursor.execute("INSERT INTO sp500tickers VALUES(?)", (ticker,))
            connection.commit()

        return tickers

    def fetch_sp500_tickers(self):
        cursor.execute("SELECT * FROM sp500tickers")

        tickers = []
        for ticker, in cursor.execute("SELECT * FROM sp500tickers"):
                tickers.append(ticker)

        return tickers

