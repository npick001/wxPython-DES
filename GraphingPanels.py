import wx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class HistogramPanel(wx.Panel):
    def __init__(self, parent):
        super(HistogramPanel, self).__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.draw_figure()

    def draw_figure(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.ax.set_title("Simple sin wave")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.canvas.draw()

