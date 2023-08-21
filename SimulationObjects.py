import random
from enum import Enum
from FIFO import FIFO
from Entity import Entity
from Distributions import Distribution
from SimulationExecutive import EventAction

## SimExec Functions
from SimulationExecutive import GetSimulationTime
from SimulationExecutive import ScheduleEventIn
from SimulationExecutive import ScheduleEventAt

class SimulationObject:
    class Type(Enum):
        DEFAULT = "SimulationObject"
        SOURCE = "Source"
        SERVER = "Server"
        SINK = "Sink"
    
    # static member variables
    m_nextID = 0
    
    def __init__(self, name):
        
        # identifiers
        self.m_name = name
        self.m_id = SimulationObject.m_nextID + 1
        SimulationObject.m_nextID += 1
        self.m_type = self.Type.DEFAULT
        
        # routing vars
        self.m_next = []
        self.m_previous = []
        pass
    
    def Arrive(self, entity : 'Entity'):
        
        message = "time = " + str(GetSimulationTime()) + "\t" + str(self.m_name) + "\tArrive\tEntity: " + str(entity.m_ID)
        print(message)
        
        self.NodeProcess(entity)
        pass

    def Depart(self, entity: 'Entity'):
        nextObj : 'SimulationObject'
        nextObj = self.GetNext()
        
        entity.SetSource(self.m_id)
        
        if(self.m_next.__len__() > 1):
            #error
            pass
        
        # CHANGE FOR ROUTING LOGIC
        nextLoc = random.randint(0, self.m_next.__len__() - 1)
        nextObj[nextLoc].Arrive(entity)        
        pass
        
    def NodeProcess(self, entity: 'Entity'):
        ## VIRTUAL FN TO BE IMPLEMENTED BY CHILDREN
        ## THIS IS AN ERROR IF CALLED
        pass        
        
    def AddNext(self, next : 'SimulationObject'):
        self.m_next.append(next)
        pass 
    def AddPrevious(self, m_previous : 'SimulationObject'):
        self.m_previous.append(m_previous)
        pass    
    
    # returns a set of simobjs
    def GetNext(self):
        return self.m_next
    def GetPrevious(self):
        return self.m_previous
    pass

### BEGIN INHERITED SIMULATION OBJECTS
class Source(SimulationObject):   
    m_entity = Entity
    
    def __init__(self, name, numGen, entity : 'Entity', arrivalDist : 'Distribution'):
        super().__init__(name)
        
        self.m_type = self.Type.SOURCE
        
        self.m_numToGen = numGen
        self.m_entity = entity
        self.m_arrivalDist = arrivalDist
        self.m_infiniteGen = False
        
        ScheduleEventIn(0.0, "Placeholder time unit", self.ArriveEA(self))
        pass    
    
    def NodeProcess(self, entity: Entity) -> None:
        ## SHOULD NEVER BE CALLED
        return super().NodeProcess(entity)
    
    class ArriveEA(EventAction):
        m_source : 'Source'
        
        def __init__(self, src : 'Source'):
            super().__init__()
            self.m_source = src
            pass
            
        def Execute(self):
            self.m_source.ArriveEM()
            pass         
        pass
    
    def ArriveEM(self):
        self.Depart(self.m_entity.New())
        
        if(self.m_infiniteGen == False):
            self.m_numToGen -= 1
            pass
        
        # collect stats later
        
        # arrival things
        if(self.m_numToGen > 0 or self.m_infiniteGen):
            arrivalDelta = self.m_arrivalDist.GetRV()
            
            message = "Scheduling source arrival event in " + str(arrivalDelta)
            print(message)

            #wxLogMessage(message)
            
            ScheduleEventIn(arrivalDelta, "Placeholder time unit", self.ArriveEA(self))
            pass
        pass
    pass

class Server(SimulationObject):
    class State(Enum):
        BUSY = 0
        IDLE = 1
    
    def __init__(self, name, serviceTime : 'Distribution'):
        super().__init__(name) 
        
        self.m_type = self.Type.SERVER  
        self.m_state = self.State.IDLE
        self.m_serviceDist = serviceTime
        
        self.m_queue = FIFO()
        pass
    
    def NodeProcess(self, entity: Entity) -> None:
        self.m_queue.AddEntity(entity)
        
        if self.m_state == self.State.IDLE:
            ScheduleEventIn(0.0, "Placeholder time unit", self.StartProcessingEA(self))
            pass
        pass
    
    # Start processing EA/EM
    class StartProcessingEA(EventAction):
        m_source : 'Server'
        
        def __init__(self, svr : 'Server'):
            super().__init__()
            self.m_source = svr
            pass
            
        def Execute(self):
            self.m_source.StartProcessingEM()
            pass         
        pass
    def StartProcessingEM(self):
        self.m_state = self.State.BUSY
        
        entity : 'Entity'
        entity = self.m_queue.GetEntity()
        
        serviceTime = self.m_serviceDist.GetRV()
        
        message = "Time: " + str(GetSimulationTime()) + "\tServer " + str(self.m_id) + "\tStart Processing\n"
        print(message)
        
        ScheduleEventIn(serviceTime, "Placeholder time unit", self.EndProcessingEA(self, entity))
        pass
    
    # End processing EA/EM
    class EndProcessingEA(EventAction):
        m_source : 'Server'
        
        def __init__(self, svr : 'Server', entity : 'Entity'):
            super().__init__()
            self.m_source = svr
            self.m_entity = entity
            pass
            
        def Execute(self):
            self.m_source.EndProcessingEM(self.m_entity)
            pass         
        pass
    def EndProcessingEM(self, entity : 'Entity'):
        self.m_state = self.State.IDLE
        
        if not self.m_queue.IsEmpty():
            ScheduleEventIn(0.0, "Placeholder time unit", self.StartProcessingEA(self))
            pass
        
        message = "Time: " + str(GetSimulationTime()) + "\tServer " + str(self.m_id) + "\tEnd Processing\n"
        print(message)
        
        self.Depart(entity)        
        pass
    
    pass

class Sink(SimulationObject):
    
    def __init__(self, name):
        super().__init__(name)
        
        self.m_type = self.Type.SINK              
        pass
    
    def NodeProcess(self, entity: Entity) -> None:
        
        message = "Deleting " + str(entity.m_ID) + "\n"
        print(message)        
        
        entity.SetDeletionTime(GetSimulationTime())        
        pass    
    pass
