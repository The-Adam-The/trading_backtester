import matplotlib.pyplot as plt

class Graph():

    def histogram(self, data, bins=100):
        plt.hist(data, bins)
        plt.show()

    # def scatter(self, x, y, price_data):
    #     plt.figure(figsize=(12, 5))
    #     plt.scatter(x, y, marker='^', c='g')
    #     plt.plot(price_data, alpha=0.7)
    #     plt.show()

        # plt.scatter(matrix_profits, matrix_signals, marker='^', c='g')