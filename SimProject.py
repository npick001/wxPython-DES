import wx
import GraphicalNode
from Entity import Entity
#from Canvas import Canvas
from GraphicalNode import GSource, GServer, GSink
from SimulationObjects import SimulationObject, Source, Server, Sink

from SimulationExecutive import GetSimulationTime

class SimulationProject:
    def __init__(self) -> None:
        pass
    pass
    
    
class NodeFactory:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def CreateGraphicalNode(cls, type : 'SimulationObject.Type', parent,  center : 'wx.Point2D', label=None) -> 'SimulationObject':
        
        entity = Entity(GetSimulationTime())
        if(type == SimulationObject.Type.SOURCE):
            source = GSource("Source", parent, center)            
            return source
        
        elif(type == SimulationObject.Type.SERVER):
            server = GServer("Server", parent, center)
            return server
        
        elif(type == SimulationObject.Type.SINK):
            sink = GSink("Sink", parent, center)
            return sink
        
        else:
            print("ERROR IN CREATEGRAPHICALNODE, TYPE DOES NOT EXIST")
            pass
        pass
    pass