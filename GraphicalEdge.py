import wx
from GraphicalElement import GraphicalElement
from GraphicalNode import GraphicalNode

class GraphicalEdge(GraphicalElement):
    def __init__(self, id, source : 'GraphicalNode', destination : 'GraphicalNode'):
        
        self.m_id = id
        self.m_source = source
        self.m_destination = destination
        
        self.m_sourcePoint : 'wx.Point2D'
        self.m_destinationPoint : 'wx.Point2D'
        
        self.m_sourceID = -1
        self.m_destinationID = -1        
        pass
    
    def SetSource(self, source : 'GraphicalNode'):
        
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
    
    def SetDestination(self, destination : 'GraphicalNode'):
        
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