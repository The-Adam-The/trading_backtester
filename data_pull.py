import pandas as pd
import pandas.io.sql
import yfinance as yf

pd.options.mode.chained_assignment = None
import sqlite3


connection = sqlite3.connect('sp500tradedata.db')
cursor = connection.cursor()

#TODO: Update databases with latest information

# cursor.execute('CREATE TABLE sp500tickers(ticker TEXT)')
# connection.commit()

class Scraper:


    def pull_sp500_list(self, number_sp=500):
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
        connection = sqlite3.connect('sp500tradedata.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sp500tickers")

        tickers = []
        for ticker, in cursor.execute("SELECT * FROM sp500tickers"):
                tickers.append(ticker)

        return tickers
#TODO: fix asset selection algorithm in scraper.fetch_sp500_data_db()
    def fetch_sp500_data_db(self, asset_names, start_date):

        df_stack = []
        db_list = []
        # connection.row_factory = sqlite3.Row
        for asset_name in asset_names:
            print(f"asset_name: {asset_name}")
            for db_name in connection.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name').fetchall():

                if db_name == ('sp500tickers',):
                    print("Ticker Table Removed")
                    continue

                if asset_name == 'all':
                    db_list.append(db_name)

                if db_name == f"TradeDate{asset_name}":
                    db_list.append(db_name)
                # else:
                    # try:
                    #     df = yf.download(asset_name, start_date)
                    #     df_stack.append([asset_name, df])
                    # except:
                    #     print("Asset not found")
                print(db_list)


        for x in db_list:
            try:
                df = pd.read_sql_query('SELECT * FROM ' + x[0], connection)
                amended_x = x[0].replace('TradeData', 'Ticker: ')
                df_stack.append([amended_x, df])
            except sqlite3.Error as e:
                continue
            except pandas.io.sql.DatabaseError:
                continue

            print(df_stack)
        return df_stack

