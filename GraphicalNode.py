import wx
import Entity
from GraphicalEdge import GraphicalEdge
from GraphicalElement import GraphicalElement
from enum import Enum
from Distributions import Distribution
from SimulationObjects import SimulationObject

class GraphicalNode(GraphicalElement):
    class SizerLocations(Enum):
        TOP_LEFT = 0
        TOP_RIGHT = 1
        BOTTOM_LEFT = 2
        BOTTOM_RIGHT = 3     
        pass
    
    def __init__(self, id, parent : 'wx.Window', center : 'wx.Point2D', text):
        
        self.m_nodeType = SimulationObject.Type.DEFAULT
        self.m_next = []
        self.m_previous = []
        self.m_properties = []
        self.m_sizers = []
        
        ## graphical characteristics
        # size
        self.m_bodySize = parent.FromDIP(wx.Size(100, 75))
        self.m_ioSize = parent.FromDIP(wx.Size(15, 15))
        self.m_sizerSize = parent.FromDIP(wx.Size(6, 6))
        # color
        self.m_bodyColor = wx.BLACK
        self.m_labelColor = wx.WHITE
        self.m_ioColor = wx.BLUE
        self.m_sizerColor = wx.RED
        # shape
        self.m_bodyShape = wx.Rect2D(-self.m_bodySize.GetWidth() / 2, -self.m_bodySize.GetHeight() / 2, self.m_bodySize.GetWidth(), self.m_bodySize.GetHeight())
        # position
        self.m_position = center
        
        ## user sizing nodes
        # TOP_LEFT
        x = self.m_position.m_x - (self.m_bodyShape.m_width / 2)
        y = self.m_position.m_y - (self.m_bodyShape.m_height / 2)
        self.m_sizers[self.SizerLocations.TOP_LEFT] = wx.Rect2D(x, y, self.m_bodyShape.m_width, self.m_bodyShape.m_height)
        # TOP_RIGHT
        x = self.m_position.m_x + (self.m_bodyShape.m_width / 2) - self.m_sizerSize.GetWidth()
        y = self.m_position.m_y - (self.m_bodyShape.m_height / 2)
        self.m_sizers[self.SizerLocations.TOP_RIGHT] = wx.Rect2D(x, y, self.m_bodyShape.m_width, self.m_bodyShape.m_height)
        # BOTTOM_LEFT
        x = self.m_position.m_x - (self.m_bodyShape.m_width / 2)
        y = self.m_position.m_y + (self.m_bodyShape.m_height / 2) - self.m_sizerSize.GetHeight()
        self.m_sizers[self.SizerLocations.TOP_RIGHT] = wx.Rect2D(x, y, self.m_bodyShape.m_width, self.m_bodyShape.m_height)        
        # BOTTOM_RIGHT
        x = self.m_position.m_x - (self.m_bodyShape.m_width / 2) - self.m_sizerSize.GetWidth()
        y = self.m_position.m_y - (self.m_bodyShape.m_height / 2) - self.m_sizerSize.GetHeight()
        self.m_sizers[self.SizerLocations.TOP_RIGHT] = wx.Rect2D(x, y, self.m_bodyShape.m_width, self.m_bodyShape.m_height)
        
        ## io nodes
        self.m_inputRect = wx.Rect2D(-self.m_bodyShape.m_width / 2 - self.m_ioSize.GetWidth() / 2, -self.m_ioSize.GetHeight() / 2,
                                     self.m_ioSize.GetWidth(), self.m_ioSize.GetHeight())
        self.m_outputRect = wx.Rect2D(self.m_bodyShape.m_width / 2 - self.m_ioSize.GetWidth() / 2, -self.m_ioSize.GetHeight() / 2,
                                     self.m_ioSize.GetWidth(), self.m_ioSize.GetHeight())
        pass
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        ## VIRTUAL FUNCTION FOR CHILDREN TO IMPLEMENT
        pass
    
    def GetProperties(self) -> list['GraphicalEdge']:
        return self.pro
    
    def AddNext(self, next : 'GraphicalNode'):
        self.m_next.append(next)
        pass
    def AddPrevious(self, previous : 'GraphicalNode'):
        self.m_previous.append(previous)
        pass 
    def GetNext(self, next : list['GraphicalNode']):
        return self.m_next   
    def GetPrevious(self, previous : list['GraphicalNode']):
        return self.m_previous  
    
    
### BEGIN INHERITED SIMULATION OBJECTS
class Source(GraphicalNode):   
    m_entity = Entity
    
    def __init__(self, name, numGen, entity : 'Entity', arrivalDist : 'Distribution'):
        super().__init__(name)
        
        self.m_type = SimulationObject.Type.SOURCE
        
        self.m_numToGen = numGen
        self.m_entity = entity
        self.m_arrivalDist = arrivalDist
        self.m_infiniteGen = False
        pass    
    pass

class Server(GraphicalNode):
    class State(Enum):
        BUSY = 0
        IDLE = 1
    
    def __init__(self, name, serviceTime : 'Distribution'):
        super().__init__(name) 
        
        self.m_type = SimulationObject.Type.SERVER  
        self.m_state = self.State.IDLE
        self.m_serviceDist = serviceTime
        pass
    pass

class Sink(GraphicalNode):
    
    def __init__(self, name):
        super().__init__(name)
        
        self.m_type = SimulationObject.Type.SINK              
        pass 
    pass    
    