import wx
import Distributions
from enum import Enum
from Entity import Entity
from Selection import Selection
from GraphicalEdge import GraphicalEdge
from GraphicalElement import GraphicalElement
from SimulationObjects import SimulationObject
from SimulationExecutive import GetSimulationTime

class GraphicalNode(GraphicalElement):
    class SizerLocations(int):
        TOP_LEFT = 0
        TOP_RIGHT = 1
        BOTTOM_LEFT = 2
        BOTTOM_RIGHT = 3     
        pass
    
    # static member variables
    m_nextID = 1
    m_cornerRadius = 10
    
    def __init__(self, name, parent : 'wx.Panel', center : 'wx.Point2D'):
        
        self.m_nodeType = SimulationObject.Type.DEFAULT
        self.m_name = name
        self.m_label = name        
        self.m_id = GraphicalNode.m_nextID
        GraphicalNode.m_nextID += 1       
        self.m_next = []
        self.m_previous = []
        self.m_properties = []
        self.m_sizers = []
        self.m_inputs = []
        self.m_outputs = []
        
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
        x = self.m_position.x - (self.m_bodyShape.width / 2)
        y = self.m_position.y - (self.m_bodyShape.height / 2)
        self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))
        # TOP_RIGHT
        x = self.m_position.x + (self.m_bodyShape.width / 2) - self.m_sizerSize.GetWidth()
        y = self.m_position.y - (self.m_bodyShape.height / 2)
        self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))
        # BOTTOM_LEFT
        x = self.m_position.x - (self.m_bodyShape.width / 2)
        y = self.m_position.y + (self.m_bodyShape.height / 2) - self.m_sizerSize.GetHeight()
        self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))    
        # BOTTOM_RIGHT
        x = self.m_position.x - (self.m_bodyShape.width / 2) - self.m_sizerSize.GetWidth()
        y = self.m_position.y - (self.m_bodyShape.height / 2) - self.m_sizerSize.GetHeight()
        self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))
        
        ## io nodes
        self.m_inputRect = wx.Rect2D(-self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2, -self.m_ioSize.GetHeight() / 2,
                                     self.m_ioSize.GetWidth(), self.m_ioSize.GetHeight())
        self.m_outputRect = wx.Rect2D(self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2, -self.m_ioSize.GetHeight() / 2,
                                     self.m_ioSize.GetWidth(), self.m_ioSize.GetHeight())
        pass
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        ## VIRTUAL FUNCTION FOR CHILDREN TO IMPLEMENT
        pass
    
    def GetInputPoint(self):
        inputPoint = wx.Point2D(self.m_inputRect.x + self.m_inputRect.width / 2,
                                self.m_inputRect.y + self.m_inputRect.height / 2)
        return self.GetTransform().TransformPoint(inputPoint)
    
    def GetOutputPoint(self):
        outputPoint = wx.Point2D(self.m_outputRect.x + self.m_outputRect.width / 2,
                                 self.m_outputRect.y + self.m_outputRect.height / 2)
        return self.GetTransform().TransformPoint(outputPoint)
    
    def DisconnectInputs(self):
        for input in self.m_inputs:
            input : 'GraphicalEdge'
            input.Disconnect()            
            pass
        pass
    
    def DisconnectOutputs(self):
        for output in self.m_outputs:
            output : 'GraphicalEdge'
            output.Disconnect()            
            pass
        pass
    
    # WRONG
    def GetProperties(self) -> list['GraphicalEdge']:
        return self.m_properties
    
    def GetTransform(self):
        transform = wx.AffineMatrix2D()
        transform.Translate(self.m_position.x, self.m_position.y)     
        return transform
    
    def AddNext(self, next : 'GraphicalNode'):
        self.m_next.append(next)
        pass
    def AddPrevious(self, previous : 'GraphicalNode'):
        self.m_previous.append(previous)
        pass 
    def GetNext(self) -> list['GraphicalNode']:
        return self.m_next   
    def GetPrevious(self) -> list['GraphicalNode']:
        return self.m_previous  
    
    def Select(self, camera : 'wx.AffineMatrix2D', clickPosition : 'wx.GraphicsContext') -> 'Selection':
        # logic for selection of a graphicalNode
        
        windowToLocal = wx.AffineMatrix2D(camera)
        windowToLocal.Concat(self.GetTransform())
        windowToLocal.Invert()
        
        clickPosition = windowToLocal.TransformPoint(clickPosition)
        
        self.m_is_selected = False
        
        if self.m_inputRect.Contains(clickPosition):
            selection = Selection(self, Selection.State.NODE_INPUT)
            return selection
        
        elif self.m_outputRect.Contains(clickPosition):
            selection = Selection(self, Selection.State.NODE_OUTPUT)
            return selection
        
        elif self.m_bodyShape.Contains(clickPosition):
            self.m_is_selected = True
            selection = Selection(self, Selection.State.NODE)
            return selection
        
        else:
            selection = Selection(None, Selection.State.NONE)
            return selection
        
    def Move(self, displacement : 'wx.Point2D'):
        
        self.m_position += displacement
        
        for output in self.m_outputs:
            
            output : 'GraphicalEdge'
            output.m_sourcePoint = self.GetOutputPoint()
            pass
        
        for input in self.m_inputs:
            
            input : 'GraphicalEdge'
            input.m_destinationPoint = self.GetInputPoint()
            pass        
        pass
    
    
### BEGIN INHERITED SIMULATION OBJECTS
class GSource(GraphicalNode):   
    m_entity = Entity
     
    def __init__(self, name, parent, center):
        super().__init__(name, parent, center)
        
        self.m_type = SimulationObject.Type.SOURCE
        
        self.m_numToGen = 10
        self.m_entity = Entity(GetSimulationTime())
        self.m_arrivalDist = Distributions.Exponential(0.25)
        self.m_infiniteGen = False
        pass    
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        ## OVERRIDDEN VIRTUAL FUNCTION 
        
        localToWindow = wx.AffineMatrix2D(camera)
        localToWindow.Concat(self.GetTransform())
        
        gc.SetTransform(gc.CreateMatrix(localToWindow))
        gc.SetPen(wx.TRANSPARENT_PEN)
        
        # draw the body 
        gc.SetBrush(wx.Brush(self.m_bodyColor))
        gc.DrawRoundedRectangle(self.m_bodyShape.x, self.m_bodyShape.y, self.m_bodyShape.width, self.m_bodyShape.height, GraphicalNode.m_cornerRadius)
        
        # draw the output rectangle
        gc.SetBrush(wx.Brush(self.m_ioColor))
        gc.DrawRectangle(self.m_outputRect.x, self.m_outputRect.y, self.m_outputRect.width, self.m_outputRect.height)
        
        #gc.SetFont(wx.NORMAL_FONT, self.m_labelColor)
        #gc.GetFullTextExtent(self.m_name)
        pass
    pass

class GServer(GraphicalNode):
    class State(Enum):
        BUSY = 0
        IDLE = 1
    
    def __init__(self, name, parent, center):
        super().__init__(name, parent, center) 
        
        self.m_type = SimulationObject.Type.SERVER  
        self.m_state = self.State.IDLE
        self.m_serviceDist = Distributions.Triangular(1, 2, 3)
        pass
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        ## OVERRIDDEN VIRTUAL FUNCTION 
        
        localToWindow = wx.AffineMatrix2D(camera) 
        localToWindow.Concat(self.GetTransform())
        
        gc.SetTransform(gc.CreateMatrix(localToWindow))
        gc.SetPen(wx.TRANSPARENT_PEN)
        
        # draw the body 
        gc.SetBrush(wx.Brush(self.m_bodyColor))
        gc.DrawRoundedRectangle(self.m_bodyShape.x, self.m_bodyShape.y, self.m_bodyShape.width, self.m_bodyShape.height, GraphicalNode.m_cornerRadius)
        
        # draw the input rectangle
        gc.SetBrush(wx.Brush(self.m_ioColor))
        gc.DrawRectangle(self.m_inputRect.x, self.m_inputRect.y, self.m_inputRect.width, self.m_inputRect.height)
        
        # draw the output rectangle
        gc.DrawRectangle(self.m_outputRect.x, self.m_outputRect.y, self.m_outputRect.width, self.m_outputRect.height)
        pass
    pass

class GSink(GraphicalNode):
    
    def __init__(self, name, parent, center):
        super().__init__(name, parent, center) 
        
        self.m_type = SimulationObject.Type.SINK              
        pass 
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        ## OVERRIDDEN VIRTUAL FUNCTION 
        
        localToWindow = wx.AffineMatrix2D(camera) 
        localToWindow.Concat(self.GetTransform())
        
        gc.SetTransform(gc.CreateMatrix(localToWindow))
        gc.SetPen(wx.TRANSPARENT_PEN)
        
        # draw the body 
        gc.SetBrush(wx.Brush(self.m_bodyColor))
        gc.DrawRoundedRectangle(self.m_bodyShape.x, self.m_bodyShape.y, self.m_bodyShape.width, self.m_bodyShape.height, GraphicalNode.m_cornerRadius)
        
        # draw the input rectangle
        gc.SetBrush(wx.Brush(self.m_ioColor))
        gc.DrawRectangle(self.m_inputRect.x, self.m_inputRect.y, self.m_inputRect.width, self.m_inputRect.height)
        pass
    pass    
    