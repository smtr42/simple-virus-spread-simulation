import matplotlib.pyplot as plt


class Grapher:
    def __init__(self):
        plt.figure(figsize=(7, 2))
        self.font = {'family': 'serif',
                     'color': 'black',
                     'weight': 'normal',
                     'size': 14,
                     'horizontalalignment': "right"
                     }
        plt.tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False,
            right=False,
            left=False,
            labelleft=False)

        plt.title('Change over time', fontdict=self.font)

    def plot_healthy(self, x, y):
        plt.plot(x, y)

    def plot_sick(self, x, y):
        plt.plot(x, y)

    def plot_recovered(self, x, y):
        plt.plot(x, y)

    def show(self):
        plt.show()


