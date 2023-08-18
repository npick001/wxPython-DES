import wx
import Canvas
import GraphicalNode
from SimulationObjects import SimulationObject, Source, Server, Sink

class SimulationProject:
    def __init__(self) -> None:
        pass
    pass
    
    
class NodeFactory:
    def CreateGraphicalNode(self, type : 'SimulationObject.Type', center : 'wx.Point2D', label) -> 'SimulationObject':
        
        if(type == SimulationObject.Type.SOURCE):
            
            pass
        elif(type == SimulationObject.Type.SERVER):
        
            pass
        elif(type == SimulationObject.Type.SINK):
        
            pass
        else:
            print("ERROR IN CREATEGRAPHICALNODE, TYPE DOES NOT EXIST")
            pass
        pass
    pass