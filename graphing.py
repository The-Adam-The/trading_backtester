import matplotlib.pyplot as plt

class Graph():

    def histogram(self, data, bins=100):
        plt.hist(data, bins)
        plt.show()

    def line_plot(self, a, b, a_label, b_label, a_color='red', b_color='green'):
        #TODO: Incorporate any number of data sets/lines for graph.line_plot
        '''Basic lineplot graph parameters (a, b, _label, b_label, a_color, b_color
        a: (required) first data set
        b: (required) second data set
        a_label: (required) Label for x line
        b_label: (required) Label of y axis
        a_color: Default='red' color of a data set
        b_color: Default='green' color of b data set
        '''

        plt.plot(a, label=a_label, color=a_color)
        plt.plot(b, label=b_label, color=b_color)
        plt.legend()
        plt.show()


    def macd_scatter(self, buy_index, buy_close, sell_index, sell_close, asset_close, asset_label ):
        '''macd_scatter: buy_index, buy_close, sell_index, sell_close, asset_close, asset_label '''

        plt.figure(figsize=(12, 4))
        plt.scatter(buy_index, buy_close, marker="^", color='green')
        plt.scatter(sell_index, sell_close, marker="v", color='red')
        plt.plot(asset_close, label=asset_label, color='k')
        plt.legend()
        plt.show()
