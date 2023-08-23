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
        self.m_source.m_outputs.append(self)
        
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
        
        pass
    
    def Select(self, camera, clickPosition):
        
        pass