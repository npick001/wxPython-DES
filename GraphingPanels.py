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
    def __init__(self, parent, size, num_bins=20, data=np.random.uniform(0, 1, 1000)):
        super(HistogramPanel, self).__init__(parent)
        
        self.m_graph_type = self.GraphType.HISTOGRAM
        self.m_data = data
        self.m_size = size
        self.m_color = "Blue"
        
        self.m_figure, self.m_ax = plt.subplots(figsize=(5, 4))
        self.m_canvas = FigureCanvas(self, -1, self.m_figure)
        self.m_sizer = wx.BoxSizer(wx.VERTICAL)
        self.m_sizer.Add(self.m_canvas, 1, wx.EXPAND)
        self.m_num_bins = num_bins
        self.SetSizer(self.m_sizer)
        self.draw_graph()
        pass

    def draw_graph(self):
        self.m_ax.clear()
        
        self.m_ax.hist(self.m_data, bins=self.m_num_bins, color=self.m_color)
        self.m_ax.set_title("Histogram of Data")
        self.m_ax.set_xlabel("Data")
        self.m_ax.set_ylabel("Frequency")
        #self.m_canvas.draw() #this shows a separate window for the graph
        self.m_ax.figure.canvas.draw()
        self.Refresh()
        pass
    
    def set_color(self, color):
        self.m_color = color
        self.draw_graph()
        pass
    
    def set_num_bins(self, num_bins):
        self.m_num_bins = num_bins
        self.draw_graph()
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