import pandas as pd
pd.options.mode.chained_assignment = None

class Scraper:

    def pull_sp500(self, number_sp=500):
        tickers = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0][: number_sp - 1]

        tickers = tickers.Symbol.to_list()
        # '.' causes errors
        tickers = [i.replace('.', '-') for i in tickers]
        return tickers
