import wx
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from enum import Enum
from Distributions import *
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
        
        self.m_theoretical_distribution = None
        self.theoretical_line_x = None
        self.theoretical_line_y = None
        
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
        
        # Plot the histogram
        self.m_ax.hist(self.m_data, bins=self.m_num_bins, color=self.m_color, density=True)
        
        # Overlay the theoretical distribution line if it exists
        if self.theoretical_line_x is not None and self.theoretical_line_y is not None:
            self.m_ax.plot(self.theoretical_line_x, self.theoretical_line_y, 'r-', lw=2)
            self.m_ax.set_title("Histogram of Data with Theoretical Distribution")
            pass
        else:
            self.m_ax.set_title("Histogram of Data")
            pass

        self.m_ax.set_xlabel("Data")
        self.m_ax.set_ylabel("Frequency")
        self.m_ax.figure.canvas.draw()
        self.Refresh()
        pass
    
    def set_theoretical_distribution(self, distribution_params, distribution_type):
        # Generate x values (data range for the line)
        x = np.linspace(min(self.m_data), max(self.m_data), 1000)
        y = []
        
        #wx.LogMessage("Distribution Type: " + str(distribution_type))
        
        # Generate y values based on the type and parameters of the theoretical distribution
        if distribution_type == Distribution.Type.NORMAL:
            
            wx.LogMessage("Normal Distribution")
            
            dist = Normal(distribution_params[0], distribution_params[1])
            for i in range(0, 1000):
                y.append(dist.GetRV())
                pass
            
            pass
        elif distribution_type == Distribution.Type.EXPONENTIAL:
            
            wx.LogMessage("Exponential Distribution")
            
            dist = Exponential(distribution_params[0])
            for i in range(0, 1000):
                y.append(dist.GetRV())
                pass
            
            pass
        elif distribution_type == Distribution.Type.UNIFORM:
            
            wx.LogMessage("Uniform Distribution")
            
            dist = Uniform(distribution_params[0], distribution_params[1])
            for i in range(0, 1000):
                y.append(dist.GetRV())
                pass
            
            pass
        elif distribution_type == Distribution.Type.TRIANGULAR:
            
            wx.LogMessage("Triangular Distribution")
            
            dist = Triangular(distribution_params[0], distribution_params[1], distribution_params[2])
            for i in range(0, 1000):
                y.append(dist.GetRV())
                pass
            
            pass
        elif distribution_type == Distribution.Type.WEIBULL:
            
            wx.LogMessage("Weibull Distribution")
            
            dist = Weibull(distribution_params[0], distribution_params[1])
            for i in range(0, 1000):
                y.append(dist.GetRV())
                pass            
            
            pass
        
        wx.LogMessage(str(len(y)))
        
        self.theoretical_line_x = x
        self.theoretical_line_y = y
        self.draw_graph()
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