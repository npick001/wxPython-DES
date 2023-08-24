import wx
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

        # EVENT HANDLERS
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
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
        sourcePos.x -= self.FromDIP(150)       
         
        serverPos = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)       
        
        sinkPos = wx.Point2D(self.m_originPoint.x, self.m_originPoint.y)
        sinkPos.x += self.FromDIP(150)  
        
        self.AddNode(SimulationObject.Type.SOURCE, wx.Point2D(sourcePos.x, sourcePos.y))
        self.AddNode(SimulationObject.Type.SERVER, wx.Point2D(serverPos.x, serverPos.y))
        self.AddNode(SimulationObject.Type.SINK, wx.Point2D(sinkPos.x, sinkPos.y))
        pass
    
    def GetCameraTransform(self) -> 'wx.AffineMatrix2D':
        
        cameraTransform = wx.AffineMatrix2D(self.m_cameraZoom) # scaling
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
        self.m_originPoint.x += dragVector.x
        self.m_originPoint.y += dragVector.y
        
        inv = wx.AffineMatrix2D(self.GetCameraTransform())
        inv.Invert()
        dragVector = inv.TransformDistance(dragVector)
        self.m_cameraPan.Translate(dragVector.x, dragVector.y)
        
        self.m_previousMousePosition = clickPosition
        
        self.Refresh()      
        pass
    
    def MoveNode(self, clickPosition):
        
        dragVector = clickPosition - self.m_previousMousePosition
        
        inv = wx.AffineMatrix2D(self.GetCameraTransform())
        # next line is not tested yet
        inv.Concat(self.m_nodes[self.m_selection])
        inv.Invert()
        dragVector = inv.TransformDistance(dragVector)
        self.m_cameraPan.Translate(dragVector.x, dragVector.y)
        
        self.m_previousMousePosition = clickPosition
        
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
    def OnMiddleDown(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the middle mouse button down event
        self.m_isPanning = True
        self.m_previousMousePosition = wx.Point2D(event.GetPosition())        
        pass
    def OnMiddleUp(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the middle mouse button up event
        self.m_isPanning = False
        pass   
    def OnLeftDown(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the left mouse button down event
        self.m_selection = self.Select(event.GetPosition())
        self.m_selectionID = self.m_selection.m_element.m_id if self.m_selection.isOK() else -1
        self.m_previousMousePosition = wx.Point2D(event.GetPosition())
        prevMousePos = wx.Point2D(self.m_previousMousePosition)
        
        # this is a world to local transformation
        self.TransformPoint(prevMousePos)
        
        self.m_debug_status_bar.SetStatusText("Zoom Level: " + str(self.m_zoomLevel), self.DebugField.ZOOM_LEVEL.value)
        self.m_debug_status_bar.SetStatusText("Mouse Position(" + str(self.m_previousMousePosition.x) + ", " 
                                              + str(self.m_previousMousePosition.y) + ")", self.DebugField.MOUSE_POSITION.value)
        
        if self.m_selection.m_state == Selection.State.NODE_INPUT:
            
            # generate a new edge and add it to the list of edges
            newEdge = GraphicalEdge(self.m_nextID, self.m_selection.m_element, None)
            self.m_elements.append(newEdge)
            self.m_edges.append(newEdge)
            
            # get the most recent incomplete edge
            self.incompleteEdge : 'GraphicalEdge'
            self.incompleteEdge = self.m_edges.pop()
            
            # set the destination node of the edge
            self.incompleteEdge.SetDestination(self.m_selection.m_element)          
            
            print("Selection state node output")
            pass
        elif self.m_selection.m_state == Selection.State.NODE_OUTPUT:
            # generate a new edge and add it to the list of edges
            newEdge = GraphicalEdge(self.m_nextID, self.m_selection.m_element, None)
            self.m_elements.append(newEdge)
            self.m_edges.append(newEdge)
            
            # get the most recent incomplete edge
            self.incompleteEdge : 'GraphicalEdge'
            self.incompleteEdge = self.m_edges.pop()
            
            # set the source node of the edge
            self.incompleteEdge.SetSource(self.m_selection.m_element)  
            print("Selection state node output")
            pass
        elif self.m_selection.m_state == Selection.State.NODE:
            
            # prepare to drag node
            # set element as selected 
            self.m_selection.m_element.SetSelected(True)
            self.m_previous_selection.m_element.SetSelected(False)
            
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
    def OnLeftUp(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the left mouse button up event    
        
        # get end selection
        end_selection = self.Select(event.GetPosition())
        
        if self.m_selection.m_state == Selection.State.NODE_INPUT:
            
            # check that the user selected an output to pair with the input and then connect
            if end_selection.m_state == Selection.State.NODE_OUTPUT and end_selection.m_element != self.incompleteEdge.m_destination:
                self.incompleteEdge.SetSource(end_selection.m_element)
                
                # once edge is connected, its no longer incomplete
                completeEdge = self.incompleteEdge
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
                self.m_edges.pop()
                pass
           
            pass
        elif self.m_selection.m_state == Selection.State.NODE_OUTPUT:
            
            # check that user selected an input to pair with the output and then connect
            if end_selection.m_state == Selection.State.NODE_INPUT and end_selection.m_element != self.incompleteEdge.m_source:
                self.incompleteEdge.SetDestination(end_selection.m_element)
                
                # once edge is connected, its no longer incomplete
                completeEdge = self.incompleteEdge
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
                self.m_edges.pop()
                pass
            pass
        elif self.m_selection.m_state == Selection.State.NODE:
            
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
    def OnMotion(self, event : 'wx.MouseEvent'):
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
                self.incompleteEdge.SetSource(self.m_selection.m_element)
                pass
            elif self.incompleteEdge:
                self.incompleteEdge.Disconnect()
                self.m_edges.pop()
                self.incompleteEdge = None
                pass
            refresh = True
            pass
        elif self.m_selection.m_state == Selection.State.NODE_OUTPUT:
            
            if event.ButtonDown(wx.MOUSE_BTN_LEFT):
                self.incompleteEdge.SetDestination(self.m_selection.m_element)
                pass
            elif self.incompleteEdge:
                self.incompleteEdge.Disconnect()
                self.m_edges.pop()
                self.incompleteEdge = None                
                pass         
            refresh = True   
            pass
        elif self.m_selection.m_state == Selection.State.NODE:
            # if left button is down then move the node
            if event.ButtonDown(wx.MOUSE_BTN_LEFT):
                self.MoveNode(mouse_position)
                pass            
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
    def OnMouseWheel(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the mouse wheel event
        mousePosition = wx.Point2D(event.GetPosition())
        
        # determine the zoom scale factor
        scaleFactor = pow((0.1 * event.GetWheelRotation() / event.GetWheelDelta()), 2)
        
        # transform point into local coords
        self.TransformPoint(mousePosition)
        
        # adjust the scale and translation of the camera for zooming based on the mouse position
        self.m_cameraPan.Translate(-mousePosition.x, -mousePosition.y)
        self.m_cameraZoom.Scale(scaleFactor, scaleFactor)
        self.m_cameraPan.Translate(mousePosition.x, mousePosition.y)
        self.m_zoomLevel = self.m_zoomLevel * scaleFactor
        
        # update the previous mouse position
        self.m_previousMousePosition = mousePosition
        self.Refresh()
        pass
    def OnRightUp(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the middle mouse button down event
        pass
    def OnLeaveWindow(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the middle mouse button down event
        pass
    def OnEnterWindow(self, event : 'wx.MouseEvent'):
        # Implement the logic to handle the middle mouse button down event
        pass
    def OnCharHook(self, event : 'wx.KeyEvent'):
        # Implement the logic to handle the middle mouse button down event
        pass
    def OnDeleteKey(self, event : 'wx.KeyEvent'):
        # Implement the logic to handle the middle mouse button down event
        pass
    