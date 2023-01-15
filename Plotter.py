import numpy as np
import matplotlib.pyplot as plt

import SA_Math

class Plotter():
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.title = "Plotter"
        self.grid = True

        self.functions = {
            "sin" : np.sin
        }


    def setPlotter(self, opt : tuple):
        pass

    def plot(self, x, y):
        self.ax.plot(x, y)
        
        plt.title(self.title)
        if self.grid:
            plt.grid()
        plt.show()


    def plotFunction(self, func : str, rangeX : list, numPoints = 100):
        if func == "sin":
            x = np.linspace(rangeX[0], rangeX[1], numPoints)
            y = np.sin(x)

        self.plot(x, y)

    def plotEquation(self, equation : str, params : tuple, rangeX : list, var = "x",  numPoints = 100):
        equation = "5*x+3"

        x = np.linsapce(rangeX[0], rangeX[1], numPoints)
        # y = np.array([ SA_Math(). for i in x])

        

    def plotDataset(self):
        pass


if __name__ == "__main__":
    # plotter = Plotter()

    func = "sin"
    rangeX = [-20, 20]
    # plotter.plotFunction(func, rangeX)

    #fig, ax = plt.subplots(projection = "3d")
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    r = np.linspace(-1, 1, 100)
    a = np.linspace(0, 2*np.pi, 100)

    r,a = np.meshgrid(r,a)

    x = np.cos(a) * (1 + r/2 * np.cos(a/2))
    y = np.sin(a) * (1 + r/2 * np.cos(a/2))
    z = r/2 * np.sin(a/2)

    # ax.plot3D(x,y,z)
    ax.plot_surface(x, y, z)

    plt.show()
