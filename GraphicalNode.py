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
    
    def __init__(self, name, center : 'wx.Point2D'):
        
        self.m_nodeType = SimulationObject.Type.DEFAULT
        self.m_name = name
        self.m_id = GraphicalNode.m_nextID
        GraphicalNode.m_nextID += 1       
        self.m_label = "GNode " + str(self.m_id)        
        self.m_next = []
        self.m_previous = []
        self.m_properties = []
        self.m_sizers = []
        self.m_inputs = []
        self.m_outputs = []
        self.m_is_selected = False
        
        ## graphical characteristics
        # size
        self.m_bodySize = wx.Size(100, 75)
        self.m_ioSize = wx.Size(15, 15)
        self.m_sizerSize = wx.Size(6, 6)
        # color
        self.m_bodyColor = wx.BLACK
        self.m_labelColor = wx.WHITE
        self.m_ioColor = wx.BLUE
        self.m_sizerColor = wx.RED
        # position
        self.m_position = wx.Point2D(center.x, center.y)
        # shape
        self.m_bodyShape = wx.Rect2D(self.m_position.x - self.m_bodySize.GetWidth() / 2, self.m_position.y - self.m_bodySize.GetHeight() / 2, 
                                     self.m_bodySize.GetWidth(), self.m_bodySize.GetHeight())
        
        ## user rotation node
        distanceFromNode = self.m_bodyShape.height * 0.75
        x = self.m_position.x - (self.m_ioSize.GetWidth() / 2)
        y = self.m_position.y - distanceFromNode - (self.m_bodyShape.height / 2) + self.m_ioSize.GetHeight()
        self.m_rotator = wx.Rect2D(x, y, self.m_ioSize.GetWidth(), self.m_ioSize.GetHeight())
        
        ## user sizing nodes
        # TOP_LEFT
        # x = self.m_position.x - (self.m_bodyShape.width / 2)
        # y = self.m_position.y - (self.m_bodyShape.height / 2)
        # self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))
        # # TOP_RIGHT
        # x = self.m_position.x + (self.m_bodyShape.width / 2) - self.m_sizerSize.GetWidth()
        # y = self.m_position.y - (self.m_bodyShape.height / 2)
        # self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))
        # # BOTTOM_LEFT
        # x = self.m_position.x - (self.m_bodyShape.width / 2)
        # y = self.m_position.y + (self.m_bodyShape.height / 2) - self.m_sizerSize.GetHeight()
        # self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))    
        # # BOTTOM_RIGHT
        # x = self.m_position.x - (self.m_bodyShape.width / 2) - self.m_sizerSize.GetWidth()
        # y = self.m_position.y - (self.m_bodyShape.height / 2) - self.m_sizerSize.GetHeight()
        # self.m_sizers.append(wx.Rect2D(x, y, self.m_bodyShape.width, self.m_bodyShape.height))
        
        ## io nodes
        self.m_inputRect = wx.Rect2D(self.m_position.x - self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2, - self.m_ioSize.GetHeight() / 2,
                                     self.m_ioSize.GetWidth(), self.m_ioSize.GetHeight())
        self.m_outputRect = wx.Rect2D(self.m_position.x + self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2, - self.m_ioSize.GetHeight() / 2,
                                     self.m_ioSize.GetWidth(), self.m_ioSize.GetHeight())
        
        self.m_inputPoint = self.GetTransform().TransformPoint(wx.Point2D(self.m_inputRect.x + self.m_inputRect.width / 2, self.m_inputRect.y + self.m_inputRect.height / 2))
        self.m_outputPoint = self.GetTransform().TransformPoint(wx.Point2D(self.m_outputRect.x + self.m_outputRect.width / 2, self.m_outputRect.y + self.m_outputRect.height / 2))
        pass
    
    def Draw(self, camera : 'wx.AffineMatrix2D', gc : 'wx.GraphicsContext'):
        ## VIRTUAL FUNCTION FOR CHILDREN TO IMPLEMENT
        pass
    
    def GetInputPoint(self):
        return self.m_inputPoint
    
    def GetOutputPoint(self):
        return self.m_outputPoint
    
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
    
    def Select(self, camera : 'wx.AffineMatrix2D', clickPosition : 'wx.Point2D') -> 'Selection':
        # logic for selection of a graphicalNode
        
        windowToLocal = wx.AffineMatrix2D(camera)
        windowToLocal.Concat(self.GetTransform())
        windowToLocal.Invert()
        
        clickPosition = windowToLocal.TransformPoint(wx.Point2D(clickPosition))
        
        self.m_is_selected = False
        
        if self.m_inputRect.Contains(clickPosition):
            selection = Selection()
            selection.m_element = self
            selection.m_state = Selection.State.NODE_INPUT           
            return selection
        
        elif self.m_outputRect.Contains(clickPosition):
            selection = Selection()
            selection.m_element = self
            selection.m_state = Selection.State.NODE_OUTPUT   
            return selection
        
        elif self.m_bodyShape.Contains(clickPosition):
            self.m_is_selected = True
            selection = Selection()
            selection.m_element = self
            selection.m_state = Selection.State.NODE   
            return selection
        
        else:
            selection = Selection()
            return selection
        
    def Move(self, xdistance, ydistance):        
        self.m_position.x += xdistance
        self.m_position.y += ydistance
        
        self.m_inputRect.x += xdistance
        self.m_inputRect.y += ydistance
        # self.m_inputPoint.x = self.m_inputRect.x + self.m_inputRect.width / 2
        # self.m_inputPoint.y = self.m_inputRect.y + self.m_inputRect.height / 2
        
        self.m_outputRect.x += xdistance
        self.m_outputRect.y += ydistance
        # self.m_outputPoint.x = self.m_outputRect.x + self.m_outputRect.width / 2
        # self.m_outputPoint.y = self.m_outputRect.y + self.m_outputRect.height / 2
        
        self.m_rotator.x += xdistance
        self.m_rotator.y += ydistance       
        
        for output in self.m_outputs:
            
            output : 'GraphicalEdge'
            # output.m_sourcePoint = self.GetOutputPoint()
            output.m_sourcePoint.x = self.m_outputPoint.x
            output.m_sourcePoint.y = self.m_outputPoint.y
            pass
        
        for input in self.m_inputs:
            
            input : 'GraphicalEdge'
            # input.m_destinationPoint = self.GetInputPoint()
            input.m_destinationPoint.x = self.m_inputPoint.x
            input.m_destinationPoint.y = self.m_inputPoint.y
            pass        
        pass
    
    
### BEGIN INHERITED SIMULATION OBJECTS
class GSource(GraphicalNode):   
    m_entity = Entity
     
    def __init__(self, name, center):
        super().__init__(name, center)
        
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
        if self.m_is_selected:
            gc.SetPen(wx.Pen(wx.BLUE, 3))
            pass
        
        ## body node
        self.m_bodyShape.x = self.m_position.x - self.m_bodySize.GetWidth() / 2
        self.m_bodyShape.y = self.m_position.y - self.m_bodySize.GetHeight() / 2

        ## io nodes
        # self.m_inputRect.x = self.m_position.x - self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2
        # self.m_inputRect.y = -self.m_ioSize.GetHeight() / 2

        self.m_outputRect.x = self.m_position.x + self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2
        self.m_outputRect.y = self.m_position.y -self.m_ioSize.GetHeight() / 2
        
        #self.m_inputPoint = self.GetTransform().TransformPoint(wx.Point2D(self.m_inputRect.x + self.m_inputRect.width / 2, self.m_inputRect.y + self.m_inputRect.height / 2))
        self.m_outputPoint = self.GetTransform().TransformPoint(wx.Point2D(self.m_outputRect.x + self.m_outputRect.width / 2, self.m_outputRect.y + self.m_outputRect.height / 2))
        
        # draw body
        gc.DrawRoundedRectangle(self.m_bodyShape.x, self.m_bodyShape.y, self.m_bodyShape.width, self.m_bodyShape.height, GraphicalNode.m_cornerRadius)
           
        gc.SetPen(wx.TRANSPARENT_PEN)
        
        # draw the output rectangle
        gc.SetBrush(wx.Brush(self.m_ioColor))
        gc.DrawRectangle(self.m_outputRect.x, self.m_outputRect.y, self.m_outputRect.width, self.m_outputRect.height)
        
        if self.m_is_selected:
            gc.SetPen(wx.Pen(wx.BLACK, 1))
            
            distanceFromNode = self.m_bodyShape.height * 0.75
            self.m_rotator.x = self.m_position.x - (self.m_ioSize.GetWidth() / 2)
            self.m_rotator.y = self.m_position.y - distanceFromNode - (self.m_bodyShape.height / 2) + self.m_ioSize.GetHeight()
            
            rotatorCenter = wx.Point2D(self.m_rotator.x + self.m_rotator.width / 2,
                                       self.m_rotator.y + self.m_rotator.height / 2)
            
            # draw path to the top rotator
            path = gc.CreatePath()
            path.MoveToPoint(self.m_position.x, self.m_position.y)
            path.AddLineToPoint(rotatorCenter.x, rotatorCenter.y)
            gc.DrawPath(path)
            
            # draw the rotator
            gc.SetBrush(wx.Brush(self.m_ioColor))
            gc.DrawRectangle(self.m_rotator.x, self.m_rotator.y, self.m_rotator.width, self.m_rotator.height)           
            pass
        
        #gc.SetFont(wx.NORMAL_FONT, self.m_labelColor)
        #gc.GetFullTextExtent(self.m_name)
        pass    
    pass

class GServer(GraphicalNode):
    class State(Enum):
        BUSY = 0
        IDLE = 1
    
    def __init__(self, name, center):
        super().__init__(name, center) 
        
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
        if self.m_is_selected:
            gc.SetPen(wx.Pen(wx.BLUE, 3))
            pass
        
         ## body node
        self.m_bodyShape.x = self.m_position.x - self.m_bodySize.GetWidth() / 2
        self.m_bodyShape.y = self.m_position.y - self.m_bodySize.GetHeight() / 2

        ## io nodes
        self.m_inputRect.x = self.m_position.x - self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2
        self.m_inputRect.y = self.m_position.y - self.m_ioSize.GetHeight() / 2

        self.m_outputRect.x = self.m_position.x + self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2
        self.m_outputRect.y = self.m_position.y - self.m_ioSize.GetHeight() / 2
        
        # draw body
        gc.DrawRoundedRectangle(self.m_bodyShape.x, self.m_bodyShape.y, self.m_bodyShape.width, self.m_bodyShape.height, GraphicalNode.m_cornerRadius)
           
        gc.SetPen(wx.TRANSPARENT_PEN)
        
        # draw the input rectangle
        gc.SetBrush(wx.Brush(self.m_ioColor))
        gc.DrawRectangle(self.m_inputRect.x, self.m_inputRect.y, self.m_inputRect.width, self.m_inputRect.height)
        
        # draw the output rectangle
        gc.SetBrush(wx.Brush(self.m_ioColor))
        gc.DrawRectangle(self.m_outputRect.x, self.m_outputRect.y, self.m_outputRect.width, self.m_outputRect.height)
        
        if self.m_is_selected:
            gc.SetPen(wx.Pen(wx.BLACK, 1))
            
            distanceFromNode = self.m_bodyShape.height * 0.75
            self.m_rotator.x = self.m_position.x - (self.m_ioSize.GetWidth() / 2)
            self.m_rotator.y = self.m_position.y - distanceFromNode - (self.m_bodyShape.height / 2) + self.m_ioSize.GetHeight()
            
            rotatorCenter = wx.Point2D(self.m_rotator.x + self.m_rotator.width / 2,
                                       self.m_rotator.y + self.m_rotator.height / 2)
            
            # draw path to the top rotator
            path = gc.CreatePath()
            path.MoveToPoint(self.m_position.x, self.m_position.y)
            path.AddLineToPoint(rotatorCenter.x, rotatorCenter.y)
            gc.DrawPath(path)
            
            # draw the rotator
            gc.SetBrush(wx.Brush(self.m_ioColor))
            gc.DrawRectangle(self.m_rotator.x, self.m_rotator.y, self.m_rotator.width, self.m_rotator.height)           
            pass
        pass
    pass

class GSink(GraphicalNode):
    
    def __init__(self, name, center):
        super().__init__(name, center) 
        
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
        if self.m_is_selected:
            gc.SetPen(wx.Pen(wx.BLUE, 3))
            pass
        
         ## body node
        self.m_bodyShape.x = self.m_position.x - self.m_bodySize.GetWidth() / 2
        self.m_bodyShape.y = self.m_position.y - self.m_bodySize.GetHeight() / 2

        ## io nodes
        self.m_inputRect.x = self.m_position.x - self.m_bodyShape.width / 2 - self.m_ioSize.GetWidth() / 2
        self.m_inputRect.y = self.m_position.y - self.m_ioSize.GetHeight() / 2
        
        # draw body
        gc.DrawRoundedRectangle(self.m_bodyShape.x, self.m_bodyShape.y, self.m_bodyShape.width, self.m_bodyShape.height, GraphicalNode.m_cornerRadius)
           
        gc.SetPen(wx.TRANSPARENT_PEN)
        
        # draw the input rectangle
        gc.SetBrush(wx.Brush(self.m_ioColor))
        gc.DrawRectangle(self.m_inputRect.x, self.m_inputRect.y, self.m_inputRect.width, self.m_inputRect.height)
        
        if self.m_is_selected:
            gc.SetPen(wx.Pen(wx.BLACK, 1))
            
            distanceFromNode = self.m_bodyShape.height * 0.75
            self.m_rotator.x = self.m_position.x - (self.m_ioSize.GetWidth() / 2)
            self.m_rotator.y = self.m_position.y - distanceFromNode - (self.m_bodyShape.height / 2) + self.m_ioSize.GetHeight()
            
            rotatorCenter = wx.Point2D(self.m_rotator.x + self.m_rotator.width / 2,
                                       self.m_rotator.y + self.m_rotator.height / 2)
            
            # draw path to the top rotator
            path = gc.CreatePath()
            path.MoveToPoint(self.m_position.x, self.m_position.y)
            path.AddLineToPoint(rotatorCenter.x, rotatorCenter.y)
            gc.DrawPath(path)
            
            # draw the rotator
            gc.SetBrush(wx.Brush(self.m_ioColor))
            gc.DrawRectangle(self.m_rotator.x, self.m_rotator.y, self.m_rotator.width, self.m_rotator.height)           
            pass
        pass
    pass    
    