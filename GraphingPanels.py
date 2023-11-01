import wx
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

## define the graphing panel interface
class GraphingPanel(wx.Panel):
    class GraphType(Enum):
        DEFAULT = 0
        HISTOGRAM = 1
        LINE = 2   
        pass    
    
    def __init__(self, parent):
        super(GraphingPanel, self).__init__(parent)
        self.m_graph_type = self.GraphType.DEFAULT        
        pass
    
    def draw_graph(self, x, y):
        pass
    pass

class HistogramPanel(GraphingPanel):
    def __init__(self, parent):
        super(HistogramPanel, self).__init__(parent)
        
        self.m_graph_type = self.GraphType.HISTOGRAM
        
        self.m_figure, self.m_ax = plt.subplots(figsize=(5, 4))
        self.m_canvas = FigureCanvas(self, -1, self.m_figure)
        self.m_sizer = wx.BoxSizer(wx.VERTICAL)
        self.m_sizer.Add(self.m_canvas, 1, wx.EXPAND)
        self.m_num_bins = 20
        self.SetSizer(self.m_sizer)
        self.draw_graph()
        pass

    def draw_graph(self, data):
        self.m_ax.hist(data, bins=self.m_num_bins)
        self.m_ax.set_title("Simple sin wave")
        self.m_ax.set_xlabel("x")
        self.m_ax.set_ylabel("y")
        self.m_canvas.draw() #this shows a separate window for the graph
        pass
    pass

class LineGraph(GraphingPanel):
    def __init__(self, parent):
        super(LineGraph, self).__init__(parent)
        
        self.m_graph_type = self.GraphType.LINE
        
        self.m_figure, self.m_ax = plt.subplots(figsize=(5, 4))
        self.m_canvas = FigureCanvas(self, -1, self.m_figure)
        
        self.m_x = []
        self.m_y = []
        self.m_title = ""
        self.m_xLabel = ""
        self.m_yLabel = ""
        
        self.m_sizer = wx.BoxSizer(wx.VERTICAL)
        self.m_sizer.Add(self.m_canvas, 1, wx.EXPAND)
        self.SetSizer(self.m_sizer)
        pass
    
    def draw_graph(self, x, y):
        self.m_ax.plot(x, y)
        self.m_ax.set_title(self.m_title)
        self.m_ax.set_xlabel(self.m_xLabel)
        self.m_ax.set_ylabel(self.m_yLabel)
        self.m_canvas.draw()
        pass   
    pass