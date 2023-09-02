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
    def CreateGraphicalNode(cls, type : 'SimulationObject.Type',  center : 'wx.Point2D', label="SimulationObject") -> 'SimulationObject':
        
        if(type == SimulationObject.Type.SOURCE):
            source = GSource(label, center)            
            return source
        
        elif(type == SimulationObject.Type.SERVER):
            server = GServer(label, center)
            return server
        
        elif(type == SimulationObject.Type.SINK):
            sink = GSink(label, center)
            return sink
        
        else:
            print("ERROR IN CREATEGRAPHICALNODE, TYPE DOES NOT EXIST")
            pass
        pass
    pass