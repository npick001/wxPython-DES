import wx
from GraphicalElement import GraphicalElement

# ASSUMES THAT GRAPHICALNODE IS DEFINED FIRST, WHICH IT SHOULD BE
# IMPORT PRIORITY ALWAYS POPULATES UPWARDS
# MORE IMPORTANT MODULES WILL IMPORT LESS IMPORTANT TO AVOID
# CIRCULAR IMPORTS
#
# i.e.: 
# - Graphical Node import GEdge and GElement
# -- GraphicalElement import Selection

class GraphicalEdge(GraphicalElement):
    
    # static member variables
    m_nextID = 1
    
    def __init__(self, source=None, destination=None):
        
        self.m_id = GraphicalEdge.m_nextID
        GraphicalEdge.m_nextID += 1 
        
        self.m_label = "GEdge " + str(self.m_id)
        
        self.SetSource(source)
        self.SetSource(destination)
        
        self.m_sourcePoint : 'wx.Point2D'
        self.m_destinationPoint : 'wx.Point2D'
        
        self.m_sourceID = -1
        self.m_destinationID = -1        
        pass
    
    def SetSource(self, source):
        
        if not source:
            return
        
        self.m_source = source
        self.m_sourceID = source.m_id
        self.m_sourcePoint = source.GetOutputPoint()
        self.m_source.m_inputs.append(self)
        
        if self.m_destination:
            return
        
        self.m_destinationPoint = self.m_sourcePoint        
        pass
    
    def SetDestination(self, destination):
        
        if not destination:
            return
        
        self.m_destination = destination
        self.m_destinationID = destination.m_id
        self.m_destinationPoint = destination.GetInputPoint()
        self.m_destination.m_outputs.append(self)
        
        if self.m_source:
            return
        
        self.m_sourcePoint = self.m_destinationPoint        
        pass
    
    def Disconnect(self):
        
        if self.m_source:
            self.m_source.m_outputs.remove(self)
            self.m_source = None            
            pass
        
        if self.m_destination:
            self.m_destination.m_inputs.remove(self)
            self.m_destination = None 
            pass
        pass
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        
        # using a copy of the camera and the graphics context,generate a line between the source and destination points
        # then draw the line
        
        gc.SetTransform(gc.CreateMatrix(wx.AffineMatrix2D(camera)))
        gc.SetPen(wx.Pen(wx.BLACK, 3))
        
        path = gc.CreatePath()
        path.MoveToPoint(self.m_sourcePoint)
        path.AddLineToPoint(self.m_destinationPoint)
        path.CloseSubpath()
        gc.StrokePath(path)
        
        label_color = wx.BLACK
        
        gc.SetFont(wx.NORMAL_FONT, label_color)
        
        text_width = 0
        text_height = 0
        gc.GetTextExtent(self.m_label, text_width, text_height)
        
        gc.DrawText(self.m_label, self.m_sourcePoint.x + (self.m_destinationPoint.x - self.m_sourcePoint.x) / 2 - text_width / 2,
		self.m_sourcePoint.y + (self.m_destinationPoint.y - self.m_sourcePoint.y) / 2 - text_height)
        pass
    
    def Select(self, camera, clickPosition):
        
        pass