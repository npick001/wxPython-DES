import wx
import Canvas
import GraphicalNode
from Entity import Entity
from GraphicalNode import GSource, GServer, GSink
from SimulationObjects import SimulationObject, Source, Server, Sink

from SimulationExecutive import GetSimulationTime

class SimulationProject:
    def __init__(self) -> None:
        pass
    pass
    
    
class NodeFactory:
    def CreateGraphicalNode(self, type : 'SimulationObject.Type', center : 'wx.Point2D', label) -> 'SimulationObject':
        
        entity = Entity(GetSimulationTime())
        if(type == SimulationObject.Type.SOURCE):
            
            return GSource()
        
        elif(type == SimulationObject.Type.SERVER):
        
            return GServer()
        
        elif(type == SimulationObject.Type.SINK):
        
            return GSink()
        
        else:
            print("ERROR IN CREATEGRAPHICALNODE, TYPE DOES NOT EXIST")
            pass
        pass
    pass