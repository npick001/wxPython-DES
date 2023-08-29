import wx
import math
from collections import deque
from enum import Enum, IntEnum
from Selection import Selection
from SimProject import NodeFactory
from GraphicalElement import GraphicalElement
from GraphicalEdge import GraphicalEdge
from GraphicalNode import GraphicalNode, GSource, GServer, GSink
from SimulationObjects import SimulationObject, Source, Server, Sink

class Canvas(wx.Panel):
    class DebugField(IntEnum):
        SELECTION_STATE = 0
        ZOOM_LEVEL = 2
        MOUSE_POSITION = 3
        COMPONENT_SELECTED = 1
        COMPONENTS_CONNECTED = 4
        
    class Enums(Enum):
        ID_ADD_NODE = 200
        ID_ADD_SOURCE = 201
        ID_ADD_SERVER = 202
        ID_ADD_SINK = 203
        ID_RENAME_NODE = 204
        ID_DELETE_NODE = 205
        ID_REMOVE_EDGE = 206
        
    def __init__(self, parent, status_bar):
        super().__init__(parent)
        
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        self.m_nextID = 0
        self.m_nodes = deque()
        self.m_edges = deque()
        self.m_elements = [] # all elements including nodes and edges
        self.m_incompleteEdge : 'GraphicalEdge'
        
        # Debug status bar used to display node information
        self.m_debug_status_bar = status_bar         
        self.m_status_bar_fields = 0

        # Popup menus
        self.m_canvasMenu = wx.Menu()
        self.m_nodeMenu = wx.Menu()
        self.m_nodeSubMenu = wx.Menu()
        self.m_ioMenu = wx.Menu()

        # Selection things
        self.m_selection = Selection()
        self.m_selectionID = -1
        self.m_previous_selection = Selection()
        self.m_previous_selectionID = -1
        self.m_previousMousePosition : 'wx.Point2D'
        
        # Viewing and transformations
        self.m_isPanning = False
        self.m_isScaling = False
        self.m_cameraPan = wx.AffineMatrix2D()
        self.m_cameraZoom = wx.AffineMatrix2D()
        self.m_originTransformation = wx.AffineMatrix2D()
        self.m_originPoint = wx.Point2D(0, 0)
        self.m_zoomLevel = 1
        self.m_canvasSize = wx.Size(800, 600)  
        
        # Grid things
        self.m_allowedDistanceFromOrigin = 1000
        self.m_numGridLines = 20
        self.m_numSubGridLines = 4
        self.m_gridLineSpacing = 0

        # EVENT HANDLERS
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # ARROW KEYS
        self.Bind(wx.EVT_KEY_DOWN, self.OnArrowKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnArrowKeyUp)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftClickUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClickDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClickUp)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleClickUp)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleClickDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        
        # self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel) not working yet
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        #self.Bind(wx.EVT_MIDDLE_DOWN, self.OnCharHook)
        #self.Bind(wx.EVT_MIDDLE_DOWN, self.OnDeleteKey)
        

        
    def AddNode(self, node_type : 'SimulationObject.Type', center : 'wx.Point2D', label=None):
        # Implement the logic to add a graphical node
        
        newObj = NodeFactory.CreateGraphicalNode(node_type, self, center, label)
        self.m_elements.append(newObj)
        self.m_nodes.append(newObj)
        self.Refresh()
        pass
        
    def InitializeOriginLocation(self, canvas_size : 'wx.Size'):
        # Implement the logic to set origin location
        self.m_canvasSize = canvas_size
        self.SetSize(canvas_size)
        
        width = self.m_canvasSize.GetWidth()
        height = self.m_canvasSize.GetHeight()
        
        x = width / 2
        y = height / 2       
        
        self.m_originPoint = wx.Point2D(0, 0)
        self.m_cameraPan.Translate(x, y)
        self.m_zoomLevel = self.m_zoomLevel * 1.3
        self.m_cameraZoom.Scale(self.m_zoomLevel, self.m_zoomLevel)
        
        ### THIS LINE NEEDS TO BE CALLED
        # REASON WHY:
        #   - IN PYTHON ALL VARIABLES ARE BY REFERENCE, 
        #     SO WHEN FN IS CALLED ON POINT THE VARIABLE DATA ITSELF IS CHANGED. 
        self.TransformPoint(self.m_originPoint)

        # add a couple of nodes
        sourcePos = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)
        sourcePos.x -= self.FromDIP(125)       
         
        serverPos = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)       
        
        sinkPos = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)
        sinkPos.x += self.FromDIP(125)  
        
        self.AddNode(SimulationObject.Type.SOURCE, wx.Point2D(sourcePos.x, sourcePos.y))
        self.AddNode(SimulationObject.Type.SERVER, wx.Point2D(serverPos.x, serverPos.y))
        self.AddNode(SimulationObject.Type.SINK, wx.Point2D(sinkPos.x, sinkPos.y))
        pass
    
    def GetCameraTransform(self) -> 'wx.AffineMatrix2D':
        
        cameraTransform = wx.AffineMatrix2D()
        cameraTransform.Concat(self.m_cameraZoom) # scaling
        cameraTransform.Concat(self.m_cameraPan) # translating
        return cameraTransform
    
    def TransformPoint(self, pointToTransform : 'wx.Point2D'):
        
        cTransform = wx.AffineMatrix2D(self.GetCameraTransform())
        cTransform.Invert()
        cTransform.TransformPoint(pointToTransform)
        pass
    
    def Select(self, clickPosition : 'wx.Point2D'):
        
        if (self.m_elements.__len__() == 0):
            selection = Selection()
            return selection
        
        selection = Selection()
        
        for element in self.m_elements:
            element : 'GraphicalElement'
            
            selection = element.Select(self.GetCameraTransform(), clickPosition)
            
            if(selection.isOK()):
                break
            pass        
        
        self.m_debug_status_bar : 'wx.StatusBar'
        self.m_debug_status_bar.SetStatusText("Selection State: " + GraphicalElement.SELECTION_STATE_NAMES[selection.m_state], self.DebugField.SELECTION_STATE.value)
        
        if not selection.isOK():
            self.m_debug_status_bar.SetStatusText("No object selected", self.DebugField.COMPONENT_SELECTED.value)
            return selection
        
        self.m_debug_status_bar.SetStatusText("Object Selected: " + selection.m_element.m_label, self.DebugField.COMPONENT_SELECTED.value)
        return selection
        
    def PanCamera(self, clickPosition):
        
        dragVector = wx.Point2D(clickPosition.x - self.m_previousMousePosition.x, clickPosition.y - self.m_previousMousePosition.y)
        
        inv = wx.AffineMatrix2D(self.GetCameraTransform())
        inv.Invert()
        dragVector = inv.TransformDistance(dragVector)
        self.m_cameraPan.Translate(dragVector.x, dragVector.y)
        
        self.m_previousMousePosition = clickPosition
        
        self.Refresh()      
        pass
    
    def MoveNode(self, node : 'GraphicalNode', dragVector : 'wx.Point2D'):     
        
        # print(f"Node position before moving: {node.m_position.x}, {node.m_position.y}")
        # print(f"X distance: {dragVector.x}")
        # print(f"Y distance: {dragVector.y}")
                
        node.Move(dragVector.x, dragVector.y)
        #print the node position after moving
        #print(f"Node position after moving: {node.m_position.x}, {node.m_position.y}")
        
        self.Refresh()
        pass
    
    def GetSimObjects(self):
        # Implement the logic to get simulation objects
        pass
        
    def GetUniqueNodes(self):
        # Implement the logic to get unique nodes
        pass
        
    def GetUniqueEdges(self):
        # Implement the logic to get unique edges
        pass
        
    def GetNextId(self):
        # Implement the logic to get the next ID
        pass
        
    def SetSimulationProject(self, parent_project):
        # Implement the logic to set the simulation project
        pass
        
    def PopulateCanvas(self, sim_objects):
        # Implement the logic to populate the canvas after XML deserialization
        pass
        
    def OnPaint(self, event : 'wx.PaintEvent'):
        # Implement the logic to handle the paint event
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc : 'wx.GraphicsContext'
        gc = wx.GraphicsContext.Create(dc)
        
        if gc:
            
            # draw where origin is as lines constrained by 10,000 units from the origin
            windowToLocal = wx.AffineMatrix2D(self.GetCameraTransform())
            gc.SetTransform(gc.CreateMatrix(windowToLocal))
            gc.SetPen(wx.Pen(wx.BLACK, 1))
            
            allowedDistanceFromOrigin = self.m_allowedDistanceFromOrigin
            numGridLines = self.m_numGridLines
            numSubGridLines = self.m_numSubGridLines
            self.m_gridLineSpacing = (self.m_allowedDistanceFromOrigin * 2) / (numGridLines * numSubGridLines)
            
            xLineLeft = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)
            xLineLeft.x -= allowedDistanceFromOrigin
            xLineRight = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)
            xLineRight.x += allowedDistanceFromOrigin
            xPath = gc.CreatePath()
            xPath.MoveToPoint(xLineLeft)
            xPath.AddLineToPoint(xLineRight)
            
            yLineTop = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)
            yLineTop.y -= allowedDistanceFromOrigin
            yLineBottom = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)
            yLineBottom.y += allowedDistanceFromOrigin
            yPath = gc.CreatePath()
            yPath.MoveToPoint(yLineTop)
            yPath.AddLineToPoint(yLineBottom)
            
            # create bounding box using lines
            # will actually bind the creation area to this later
            bb_width = 2 * allowedDistanceFromOrigin
            bb_height = 2 * allowedDistanceFromOrigin
            bb_x = xLineLeft.x
            bb_y = yLineTop.y
            gc.DrawRectangle(bb_x, bb_y, bb_width, bb_height)
            
            # set pen as black with 60% opacity
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 153), 1))
            
            # draw the grid lines for x and y axis
            # x axis
            for i in range(1, numGridLines):
                y = yLineTop.y + (i * (bb_height / numGridLines))
                
                topPoint = wx.Point2D(xLineLeft.x, y)
                bottomPoint = wx.Point2D(xLineRight.x, y)  
                
                thisLinePath = gc.CreatePath()
                thisLinePath.MoveToPoint(topPoint)
                thisLinePath.AddLineToPoint(bottomPoint)
                gc.StrokePath(thisLinePath)  
                pass
            
            gc.SetPen(wx.Pen(wx.LIGHT_GREY, 1))
            # draw sub grid lines for x axis
            for i in range(1, numSubGridLines * numGridLines):
                y = yLineTop.y + (i * (bb_height / (numSubGridLines * numGridLines)))
                
                topPoint = wx.Point2D(xLineLeft.x, y)
                bottomPoint = wx.Point2D(xLineRight.x, y)  
                
                thisLinePath = gc.CreatePath()
                thisLinePath.MoveToPoint(topPoint)
                thisLinePath.AddLineToPoint(bottomPoint)
                gc.StrokePath(thisLinePath)  
                pass
            
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 153), 1))
            # y axis
            for i in range(1, numGridLines):
                x = xLineLeft.x + (i * (bb_width / numGridLines))
                
                leftPoint = wx.Point2D(x, yLineTop.y)
                rightPoint = wx.Point2D(x, yLineBottom.y)       
                
                thisLinePath = gc.CreatePath()
                thisLinePath.MoveToPoint(leftPoint)
                thisLinePath.AddLineToPoint(rightPoint)
                gc.StrokePath(thisLinePath)         
                pass    
            
            gc.SetPen(wx.Pen(wx.LIGHT_GREY, 1))
            # draw sub grid lines for y axis
            for i in range(1, numSubGridLines * numGridLines):
                x = xLineLeft.x + (i * (bb_width / (numSubGridLines * numGridLines)))
                
                leftPoint = wx.Point2D(x, yLineTop.y)
                rightPoint = wx.Point2D(x, yLineBottom.y)       
                
                thisLinePath = gc.CreatePath()
                thisLinePath.MoveToPoint(leftPoint)
                thisLinePath.AddLineToPoint(rightPoint)
                gc.StrokePath(thisLinePath)         
                pass           
            
            gc.SetPen(wx.Pen(wx.BLACK, 1))
            gc.StrokePath(xPath)
            gc.StrokePath(yPath)
            # draw nodes
            for node in self.m_nodes:
                node : 'GraphicalNode'
                #print(f"Drawing node: {node.m_name}")
                #print(f"Added node at: {node.m_position.x}, {node.m_position.y}")
                node.Draw(self.GetCameraTransform(), gc)
                pass 
            
            # draw edges
            for edge in self.m_edges:
                edge : 'GraphicalEdge'
                edge.Draw(self.GetCameraTransform(), gc)
                pass
            pass      
        pass
    def OnSize(self, event : 'wx.SizeEvent'):
        self.Refresh()
        pass
    def OnMiddleClickDown(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the middle mouse button down event
        self.m_isPanning = True
        self.m_previousMousePosition = wx.Point2D(event.GetPosition())        
        pass
    def OnMiddleClickUp(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the middle mouse button up event
        self.m_isPanning = False
        pass   
    def OnLeftClickDown(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the left mouse button down event
        self.m_selection = self.Select(event.GetPosition())
        self.m_selectionID = self.m_selection.m_element.m_id if self.m_selection.isOK() else -1
        self.m_previousMousePosition = wx.Point2D(event.GetPosition())
        prevMousePos = wx.Point2D(self.m_previousMousePosition)
        
        # this is a world to local transformation
        self.TransformPoint(prevMousePos)
        
        self.m_debug_status_bar.SetStatusText("Zoom Level: " + str(self.m_zoomLevel), self.DebugField.ZOOM_LEVEL.value)
        self.m_debug_status_bar.SetStatusText("Mouse Position(" + str(prevMousePos.x) + ", " 
                                            + str(prevMousePos.y) + ")", self.DebugField.MOUSE_POSITION.value)
        
        if self.m_selection.m_state == Selection.State.NODE_INPUT:
            
            self.m_incompleteEdge = GraphicalEdge()
            
            # set the destination node of the edge
            self.m_incompleteEdge.SetDestination(self.m_selection.m_element)       
            self.m_incompleteEdge.m_sourcePoint = prevMousePos   
            print("Selection state node output")
            pass
        elif self.m_selection.m_state == Selection.State.NODE_OUTPUT:            

            self.m_incompleteEdge = GraphicalEdge()
            
            # set the source node of the edge
            self.m_incompleteEdge.SetSource(self.m_selection.m_element)  
            self.m_incompleteEdge.m_destinationPoint = prevMousePos
            print("Selection state node output")
            pass
        elif self.m_selection.m_state == Selection.State.NODE:
            
            # prepare to drag node
            # set element as selected 
            self.m_selection.m_element.SetSelected(True)
            self.m_previous_selection = self.m_selection
            
            for node in self.m_nodes:
                node : 'GraphicalNode'
                if node != self.m_selection.m_element:
                    node.SetSelected(False)
                    pass
                pass
            
            print("Selection state node")
            pass
        elif self.m_selection.m_state == Selection.State.NONE:
            self.m_isPanning = True
            print("Selection state none")
            pass
        else:
            print("SELECTION STATE ERROR IN OnLeftDown IN THE CANVAS OBJECT")
            pass
        
        self.m_previous_selection = self.m_selection
        
        self.Refresh()        
        pass
    def OnLeftClickUp(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the left mouse button up event    
        
        # get end selection
        end_selection = self.Select(event.GetPosition())
        
        if self.m_selection.m_state == Selection.State.NODE_INPUT:
            
            # check that the user selected an output to pair with the input and then connect
            if end_selection.m_state == Selection.State.NODE_OUTPUT and end_selection.m_element != self.m_selection.m_element:
                self.m_incompleteEdge.SetSource(end_selection.m_element)
                
                # once edge is connected, its no longer incomplete
                completeEdge = self.m_incompleteEdge
                # add the complete edge to the list of edges
                self.m_edges.append(completeEdge)
                
                # for this selection add next and for end selection add previous for connected nodes
                completeEdge.m_source.AddNext(completeEdge.m_destination)
                completeEdge.m_destination.AddPrevious(completeEdge.m_source)
                
                # set the debug status bar letting the user know which nodes are connected
                self.m_debug_status_bar.SetStatusText("Connected: " + completeEdge.m_source.m_label + " to " + completeEdge.m_destination.m_label, 
                                                      self.DebugField.COMPONENTS_CONNECTED.value)
                pass
            else:
                # erase the incomplete edge from the list of edges
                #self.m_edges.pop()
                pass
           
            pass
        elif self.m_selection.m_state == Selection.State.NODE_OUTPUT:
            
            # check that user selected an input to pair with the output and then connect
            if end_selection.m_state == Selection.State.NODE_INPUT and end_selection.m_element != self.m_selection.m_element:
                self.m_incompleteEdge.SetDestination(end_selection.m_element)
                
                # once edge is connected, its no longer incomplete
                completeEdge = self.m_incompleteEdge
                # add the complete edge to the list of edges
                self.m_edges.append(completeEdge)
                self.m_elements.append(completeEdge)
                
                # for this selection add next and for end selection add previous for connected nodes
                completeEdge.m_source.AddNext(completeEdge.m_destination)
                completeEdge.m_destination.AddPrevious(completeEdge.m_source)
                
                # set the debug status bar letting the user know which nodes are connected
                self.m_debug_status_bar.SetStatusText("Connected: " + completeEdge.m_source.m_label + " to " + completeEdge.m_destination.m_label, 
                                                      self.DebugField.COMPONENTS_CONNECTED.value)
                pass
            else:
                # erase the incomplete edge from the list of edges
                #self.m_edges.pop()
                pass
            pass
        elif self.m_selection.m_state == Selection.State.NODE:
            
            #dragVector = wx.Point2D(event.GetPosition().x - self.m_previousMousePosition.x, event.GetPosition().y - self.m_previousMousePosition.y)
            
            #self.MoveNode(dragVector)
            pass
        elif self.m_selection.m_state == Selection.State.NONE:
            # user is no longer panning camera
            pass
        else:
            print("SELECTION STATE ERROR IN OnLeftUp IN THE CANVAS OBJECT")
            pass
        
        self.m_isPanning = False
        self.m_isScaling = False
        self.m_selection.Reset()
        self.m_incompleteEdge = None        
        
        self.Refresh()
        pass
    def OnMouseMotion(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the mouse motion event
        mouse_position = wx.Point2D(event.GetPosition())
        refresh = False
        
        self.TransformPoint(mouse_position)
        
        # capture the mouse movement for panning and moving graphical nodes
        if self.m_isPanning:
            
            self.PanCamera(mouse_position)
            refresh = True 
            pass
        elif not self.m_selection.isOK():
            return
         
        if self.m_selection.m_state == Selection.State.NODE_INPUT:
           
            if event.ButtonDown(wx.MOUSE_BTN_LEFT):
                self.m_incompleteEdge.m_sourcePoint = self.TransformPoint(wx.Point2D(mouse_position))
                pass
            elif self.m_incompleteEdge != None:
                self.m_incompleteEdge.Disconnect()
                self.m_incompleteEdge = None
                pass
            refresh = True
            pass
        elif self.m_selection.m_state == Selection.State.NODE_OUTPUT:
            
            if event.ButtonDown(wx.MOUSE_BTN_LEFT):
                self.m_incompleteEdge.m_sourcePoint = self.TransformPoint(wx.Point2D(mouse_position))
                pass
            elif self.m_incompleteEdge != None:
                self.m_incompleteEdge.Disconnect()
                self.m_incompleteEdge = None                
                pass         
            refresh = True   
            pass
        elif self.m_selection.m_state == Selection.State.NODE:
            
            dragVector = wx.Point2D(mouse_position.x - self.m_previousMousePosition.x, mouse_position.y - self.m_previousMousePosition.y)
            
            # Movement is not moving with mouse
            # need to scale it down
            dragVector.x *= 0.375
            dragVector.y *= 0.375
            
            # so i could not get the dragvector working for movement just yet
            # i want to add movement based on the arrow keys
            # each key press will move the node by a certain number of gridlines
            # which will be user configurable => LATER
            self.MoveNode(self.m_selection.m_element, dragVector)
            
            self.m_previousMousePosition = mouse_position
            
            refresh = True
            pass
        elif self.m_selection.m_state == Selection.State.NONE:

            pass
        else:
            print("SELECTION STATE ERROR IN OnLeftUp IN THE CANVAS OBJECT")
            pass
         
        if refresh:
            self.Refresh()
            pass         
        pass
    
    ## NOT WORKING
    def OnMouseWheel(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the mouse wheel event
        mousePosition = wx.Point2D(event.GetPosition())
        
        # determine the zoom scale factor
        scaleFactor = pow((0.01 * event.GetWheelRotation() / event.GetWheelDelta()), 2)
        
        center = wx.Point2D(self.m_originPoint)
        
        # adjust the scale and translation of the camera for zooming based on the mouse position
        self.m_cameraPan.Translate(center.x, center.y)
        self.m_cameraZoom.Scale(scaleFactor, scaleFactor)
        self.m_cameraPan.Translate(-center.x, -center.y)
        self.m_zoomLevel = self.m_zoomLevel * scaleFactor
        
        # update the previous mouse position
        self.m_previousMousePosition = mousePosition
        self.Refresh()
        pass
    
    def OnArrowKeyDown(self, event : 'wx.KeyEvent'):
        
        keycode = event.GetKeyCode()
        
        if keycode == wx.WXK_UP:
            print("Up arrow pressed")
            pass
        elif keycode == wx.WXK_DOWN:
            print("Down arrow pressed")
            pass
        elif keycode == wx.WXK_LEFT:
            print("Left arrow pressed")
            pass
        elif keycode == wx.WXK_RIGHT:
            print("Right arrow pressed")
            pass
        
        event.Skip()       
        pass
    
    def OnArrowKeyUp(self, event : 'wx.KeyEvent'):
        
        keycode = event.GetKeyCode()
        
        if keycode == wx.WXK_UP:
            #print("Up arrow released")
            pass
        elif keycode == wx.WXK_DOWN:
            #print("Down arrow released")
            pass
        elif keycode == wx.WXK_LEFT:
            #print("Left arrow released")
            pass
        elif keycode == wx.WXK_RIGHT:
            #print("Right arrow released")
            pass 
        
        event.Skip()       
        pass
    
    def OnRightClickUp(self, event : 'wx.MouseEvent'):
        pass
    def OnLeaveWindow(self, event : 'wx.MouseEvent'):
        pass
    def OnEnterWindow(self, event : 'wx.MouseEvent'):
        pass
    def OnCharHook(self, event : 'wx.KeyEvent'):
        pass
    def OnDeleteKey(self, event : 'wx.KeyEvent'):
        pass
