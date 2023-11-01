import wx
import Distributions
from Entity import Entity
from Canvas import Canvas
from GraphicalNode import GraphicalNode, GSource, GServer, GSink
from SimulationObjects import SimulationObject, Source, Server, Sink
from Visitor import *
from GraphingPanels import LineGraph

from SimulationExecutive import GetSimulationTime, RunSimulation, TimeUnit

# Define the MVC Controller class.

# - The Model-View-Controller Design Pattern
# - The key roles of a SimProject are:
# 	-- build the simulation code from user graphical input
# 		--- let user know if the graphical model is a valid configuration.
# 	-- execute the built simulation code
# 		--- UI will go through controller to control simulation execution
# 	-- maintain a Canvas
# 		--- which contains the model graphical information
# 	-- manage data flow
# 		--- obtaining current simulation state from the Model
# 		--- sending simulation state information to View (UI for User)
# - Class members are broken up into Model and View sections
class SimulationProject:
    def __init__(self) -> None:
        
        self.m_model_unit = TimeUnit.MINUTES
        self.m_node_map = {} # map of GNodes to SimulationObjects
        self.m_has_been_built = False
        
        # model
        self.m_instantiated_nodes = []
        # view
        self.m_canvas = None
        pass
    
    def SetCanvas(self, canvas : 'Canvas') -> None:
        self.m_canvas = canvas
        self.m_canvas.SetSimulationProject(self)
        pass
    
    def ViewCanvas(self) -> 'Canvas':
        return Canvas(self.m_canvas)
    
    def Build(self) -> None:
        
        self.m_instantiated_nodes.clear()
        self.m_node_map.clear()
        
        roots = []
        gnodes = self.m_canvas.GetSimObjects()
        
        # find the roots of the graph
        for node in gnodes:
            node : 'GraphicalNode'
            if(node.m_type == SimulationObject.Type.SOURCE):
                roots.append(node)
                continue
            pass

        # get all the nodes for linking later
        roots_to_link = roots.copy()
        
        # build all the roots children
        for root in roots:
            root : 'GraphicalNode'
            self._BuildChildren(root)
            pass
        
        self._LinkChildren(roots_to_link)
        self.m_has_been_built = True        
        pass
    
    def CheckBuildViability(self) -> bool:
        pass
    
    def Run(self, mainframe) -> list:
        RunSimulation()
        
        # prompt the user for what file name they want to use to save the stats to
        # then write the stats to the file
        dlg = wx.FileDialog(self.m_canvas, "Save Simulation Statistics", "", "", "Text files (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        else:
            self.WriteSimulationStatistics(dlg.GetPath())
            pass
        
        return self.GraphSimulationStatistics(mainframe)
    
    def WriteSimulationStatistics(self, filename : str) -> None:
        
        # create the visitor
        visitor = StatisticsVisitor()
        
        for node in self.m_instantiated_nodes:
            node : 'SimulationObject'
            
            # accept returns a list of pairs
            # the pairs are (string, float)
            # then that needs to be written to the file
            stats = node.Accept(visitor)
            
            Utility.write_to_file(filename, node.m_name + "\n", 'a')  
            
            stats : list
            first = True
            for stat in stats:
                stat : tuple
                Utility.write_to_file(filename, stat[0] + ": " + str(stat[1]) + "\n", 'a')
                pass
            
            Utility.write_to_file(filename, "\n", 'a')          
            pass
        pass
    
    def HasBeenBuilt(self) -> bool:
        return self.m_has_been_built
    
    def RegisterNewConnection(self, source : 'GraphicalNode', target : 'GraphicalNode') -> None:
        
        # check if both nodes are instantiated
        if(self.m_node_map.get(source) == None or self.m_node_map.get(target) == None):
            self.m_has_been_built = False
            pass
        
        self.m_node_map[source].AddNext(self.m_node_map[target])
        self.m_node_map[target].AddPrevious(self.m_node_map[source])
        pass
    
    def RegisterNodeDeletion(self, to_delete : 'SimulationObject') -> None:
        sim_obj = self.m_node_map.get(to_delete)
        gnode = self.m_node_map.pop(to_delete)
        
        if sim_obj is not None:
            self.m_instantiated_nodes.remove(sim_obj)
        pass
    
    def _BuildChildren(self, root) -> None:
        
        if(self.m_node_map.get(root) != None):
            return
        else:
            
            # create the simulation object
            sim_obj = NodeFactory.CreateSimulationObject(root.m_type)
            
            # get previous nodes
            previous_nodes = sim_obj.GetPrevious()
            
            # create if statement for node type
            if(root.m_type == SimulationObject.Type.SOURCE):
                
                gsource : 'GSource'
                gsource = root
                
                src : 'Source'
                src = sim_obj
                
                # link data
                src.m_id = gsource.m_id
                src.m_entity = gsource.m_entity
                src.m_numToGen = gsource.m_numToGen
                src.m_arrivalDist = gsource.m_arrivalDist
                
                # add node to map and instantiated nodes
                self.m_node_map[gsource] = src
                self.m_instantiated_nodes.append(src)
                
                pass
            elif(root.m_type == SimulationObject.Type.SERVER):
                
                gserver : 'GServer'
                gserver = root
                
                server : 'Server'
                server = sim_obj
                
                # link data
                server.m_id = gserver.m_id
                server.m_serviceDist = gserver.m_serviceDist
                
                # add node to map and instantiated nodes
                self.m_node_map[gserver] = server
                self.m_instantiated_nodes.append(server)
                
                pass
            elif(root.m_type == SimulationObject.Type.SINK):
                
                gsink : 'GSink'
                gsink = root
                
                sink : 'Sink'
                sink = sim_obj
                
                # add node to map and instantiated nodes
                self.m_node_map[gsink] = sink
                self.m_instantiated_nodes.append(sink)
                
                pass
            
            # check if there are nodes next
            if(len(root.m_next) > 0):
                for next_node in root.m_next:
                    self._BuildChildren(next_node)
                    pass
                pass           
            pass
        pass
    
    def _LinkChildren(self, list_of_children) -> None:
        
        roots = list_of_children
        
        for root in roots:
            root : 'GraphicalNode'
            children = root.GetNext()
            nextRoots = children.copy()
            
            for child in children:
                child : 'GraphicalNode'
                
                self.m_node_map[root].AddNext(self.m_node_map[child])
                self.m_node_map[child].AddPrevious(self.m_node_map[root])
                pass
            
            if(len(nextRoots) > 0):
                self._LinkChildren(nextRoots)
                pass
            pass
        pass
    
    def GraphSimulationStatistics(self, mainframe) -> list:
        
        stat_panels = []
        
        # find all the simulation objects with graphable statistics
        for simobj in self.m_instantiated_nodes:
            simobj : 'SimulationObject'
            if(simobj.HasGraphableStatistics()):
                if(simobj.m_type == SimulationObject.Type.SERVER):

                    simobj : 'Server'
                    
                    state_chart = LineGraph(mainframe)
                    state_chart.m_x = simobj.gsm_event_times
                    state_chart.m_y = simobj.gsm_state_trajectory
                    
                    self.m_xLabel = "Event Time"
                    self.m_yLabel = "State value"
                    state_chart.m_title = simobj.m_name + " State Trajectory"                    
                    
                    stat_panels.append(state_chart)
                    pass    
                ## elif(other simulation objects with graphable statistics)
                pass
            pass
        return stat_panels  
    pass
    
    
class NodeFactory:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def CreateGraphicalNode(cls, type : 'SimulationObject.Type',  center : 'wx.Point2D', label="SimulationObject") -> 'SimulationObject':
        
        if(type == SimulationObject.Type.SOURCE):
            source = GSource("Source", center)            
            return source
        
        elif(type == SimulationObject.Type.SERVER):
            server = GServer("Server", center)
            return server
        
        elif(type == SimulationObject.Type.SINK):
            sink = GSink("Sink", center)
            return sink
        
        else:
            print("ERROR IN CREATEGRAPHICALNODE, TYPE DOES NOT EXIST")
            pass
        pass
    
    @classmethod
    def CreateSimulationObject(cls, type : 'SimulationObject.Type') -> 'SimulationObject':
        
        if(type == SimulationObject.Type.SOURCE):
            source = Source("Source", 10, Entity(GetSimulationTime()), Distributions.Exponential(1))
            return source
        
        elif(type == SimulationObject.Type.SERVER):
            server = Server("Server", Distributions.Triangular(1, 2, 3))
            return server
        
        elif(type == SimulationObject.Type.SINK):
            sink = Sink("Sink")
            return sink
        
        else:
            print("ERROR IN CREATESIMULATIONOBJECT, TYPE DOES NOT EXIST")
            pass
        pass
    pass