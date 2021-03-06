import pandas as pd
import pandas.io.sql
import yfinance as yf
pd.options.mode.chained_assignment = None
import sqlite3


connection = sqlite3.connect('sp500tradedata.db')
cursor = connection.cursor()


#TODO: Store produced data to SQL db

class DataPull:

    def pull_sp500_list(self, number_sp=500):
        tickers_connection = sqlite3.connect('sp500tickers.db')
        cursor = tickers_connection.cursor()

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
        connection = sqlite3.connect('sp500tickers.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sp500tickers")

        tickers = []
        for ticker, in cursor.execute("SELECT * FROM sp500tickers"):
                tickers.append(ticker)

        return tickers

    def pull_yahoo_data(self, assets, df_stack):

        for asset in assets:

            ydf1 = yf.download(asset[0], start=asset[1], end=asset[2])
            ydf2 = yf.download(asset[0], start=asset[3], end=asset[4])

            frames = [ydf1, ydf2]

            ydf = pd.concat(frames)
            ydf.to_sql(asset[0], connection, if_exists='append')

            for df in df_stack:
                if df[0] == asset[0]:
                    frames.append(df[1])
                    df[1] = pd.concat(frames)

        return df_stack



    #TODO: Resolve issue with tickers that contain '.' or '-' BRK-B and BF-B as they cause sql errors
    def fetch_sp500_data_db(self, asset_names, start_date, end_date):

        df_stack = []
        db_list = []
        date_range_out = []

        for asset_name in asset_names:

            if asset_name.lower() == 'all_assets':
                db_list = connection.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name').fetchall()

            else:
                for db_name in connection.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name').fetchall():

                    if db_name[0] == asset_name:
                        print(f"Database Found for {db_name[0]}\n")
                        db_list.append(db_name)


        for x in db_list:
            try:
                df = pd.read_sql_query("SELECT * FROM " + x[0] + " WHERE Date BETWEEN " + "date('" + start_date + "') AND date('" + end_date + "')",
                                       connection)

                amended_tail = df.tail(1)['Date'].values[0][0:10]
                amended_head = df.head(1)['Date'].values[0][0:10]

                temp_list = []

                #TODO: Amend pull to reflect weekends and bank holidays
                if amended_tail < end_date:
                    print(f"End date not available on Database for {x[0]}. End date: {end_date} Latest database entry: {amended_tail}\n")
                    temp_list.append(amended_tail)
                    temp_list.append(end_date)

                if amended_head > start_date:
                    print(f"Start date not available on Database for {x[0]}. Start_date: {start_date}. Earliest data entry: {amended_head}\n")
                    temp_list.append(start_date)
                    temp_list.append(amended_head)

                temp_list.insert(0, x[0])
                date_range_out.append(temp_list)
                df_stack.append([x[0], df])

            except sqlite3.Error as e:
                continue
            except pandas.io.sql.DatabaseError:
                continue
        #
        # additional_data_input = input(f"Your stored data is out of range from the dates selected for {len(date_range_out)} asset(s). Do you want to try and pull additional data(y/n)?")
        additional_data_input = "n"
        if additional_data_input.lower() == 'y':
            df_stack = self.pull_yahoo_data(date_range_out, df_stack)

        return df_stack

