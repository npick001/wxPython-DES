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
    def __init__(self, id, source=None, destination=None):
        
        self.m_id = id
        self.m_label = "GEdge " + str(self.m_id)
                
        self.m_source = source
        self.m_destination = destination
        self.m_sourcePoint = wx.Point2D(0, 0)
        self.m_destinationPoint = wx.Point2D(0, 0)
        
        self.m_sourceID = -1
        self.m_destinationID = -1  
        
        self.SetSource(source)
        self.SetDestination(destination)
        pass
    
    def SetSource(self, source):
        
        if source == None:
            print("Source is None")
            return
        
        self.m_source = source
        self.m_sourceID = source.m_id
        self.m_sourcePoint = source.GetOutputPoint()
        self.m_source.m_inputs.append(self)
        
        if self.m_destination != None:
            return
        
        self.m_destinationPoint = wx.Point2D(self.m_sourcePoint)    
        
        # print("Source: " + str(self.m_source.m_id) + "\tDestination: " + (str(self.m_destination.m_id) if self.m_destination != None else "None"))
        # print("Source Point: " + str(self.m_sourcePoint.x) + ", " + str(self.m_sourcePoint.y))
        # print("Destination Point: " + str(self.m_destinationPoint.x) + ", " + str(self.m_destinationPoint.y))
        pass
    
    def SetDestination(self, destination):
        
        if destination == None:
            print("Destination is None")
            return
        
        self.m_destination = destination
        self.m_destinationID = destination.m_id
        self.m_destinationPoint = destination.GetInputPoint()
        self.m_destination.m_outputs.append(self)
        
        if self.m_source != None:
            return
        
        self.m_sourcePoint = wx.Point2D(self.m_destinationPoint)        
        
        # print("Source: " + (str(self.m_source.m_id) if self.m_source != None else "None") + " Destination: " + str(self.m_destination.m_id))
        # print("Source Point: " + str(self.m_sourcePoint.x) + ", " + str(self.m_sourcePoint.y))
        # print("Destination Point: " + str(self.m_destinationPoint.x) + ", " + str(self.m_destinationPoint.y))
        pass
    
    def Disconnect(self):
        
        if self.m_source:
            self.m_source.m_outputs.clear()
            self.m_source = None            
            pass
        
        if self.m_destination:
            self.m_destination.m_inputs.clear()
            self.m_destination = None 
            pass
        pass
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        
        # using a copy of the camera and the graphics context,generate a line between the source and destination points
        # then draw the line
        
        gc.SetTransform(gc.CreateMatrix(wx.AffineMatrix2D(camera)))
        gc.SetPen(wx.Pen(wx.BLACK, 2))
        
        path : 'wx.GraphicsPath'
        path = gc.CreatePath()
        path.MoveToPoint(self.m_sourcePoint)
        path.AddLineToPoint(self.m_destinationPoint)
        path.CloseSubpath()
        gc.StrokePath(path)
        
        label_color = wx.BLACK
        
        gc.SetFont(wx.NORMAL_FONT, label_color)
        
        text_width = 2
        text_height = 2
        #gc.GetTextExtent(self.m_label, text_width, text_height)
        
        gc.DrawText(self.m_label, self.m_sourcePoint.x + (self.m_destinationPoint.x - self.m_sourcePoint.x) / 2 - text_width / 2,
		            self.m_sourcePoint.y + (self.m_destinationPoint.y - self.m_sourcePoint.y) / 2 - text_height)
        pass
    
    def Select(self, camera, clickPosition):
        
        pass