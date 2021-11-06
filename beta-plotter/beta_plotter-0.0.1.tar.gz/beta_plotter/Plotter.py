import numpy as np
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, equation):
        self.equation = equation
        self.x = np.arange(-100, 101)
        self.y = np.zeros_like(self.x)
        self.get_function()

    def get_function(self):
        if "x^2" in self.equation:
            a_, rest = self.equation.split("=")[1].split("x^2")
            b_, c_ = rest.split("x")
            a_, b_, c_ = int(a_), int(b_), int(c_)
            self.quadratic(a_, b_, c_)
        elif "x" in self.equation:
            slope, intercept = self.equation.split("=")[1].split("x")
            slope, intercept = int(slope), int(intercept)
            self.linear(slope, intercept)

    def linear(self, slope, intercept):
        self.y = slope * self.x + intercept

    def quadratic(self, a_, b_, c_):
        self.y = a_ * (self.x ** 2) + b_ * self.x + c_

    def plot_line(self):
        plt.plot(self.x, self.y)
        plt.show()


def main():
    equation = Plot("y=2x^2+3x+5")
    equation.plot_line()


if __name__ == "__main__":
    main()
