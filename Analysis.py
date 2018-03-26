import numpy as np
import matplotlib.pyplot as plt


class Analysis:

    @staticmethod
    def mean_squared_error(original, output):
        return np.square(np.subtract(original, output)).mean()

    @staticmethod
    def draw_plot(x, y, xlabel, ylabel, name):
        plt.plot(x, y)
        ax = plt.subplot(111)
        ax.set_xlim([0, max(x)])
        ax.set_ylim([0.9*min(y), 1.05*max(y)])
        ax.grid(linestyle='dashed')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(name + ".png", bbox_inches='tight')


class FilterProps:

    def __init__(self, gamma, gauss):
        self.gamma = gamma
        self.gauss = gauss
