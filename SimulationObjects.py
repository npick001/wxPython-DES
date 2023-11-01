import random
from Visitor import *
from enum import Enum
from FIFO import FIFO
from Entity import Entity
from Distributions import Distribution
from SimulationExecutive import EventAction

## SimExec Functions
from SimulationExecutive import GetSimulationTime
from SimulationExecutive import ScheduleEventIn
from SimulationExecutive import ScheduleEventAt
from Visitor import Visitor

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
        
        # statistics handling
        self.sm_time_utilized = 0
        self.sm_time_starved = 0
        self.sm_resource_utilization = 0
        pass
    
    def Accept(self, visitor : 'Visitor'):
        pass
    
    def HasGraphableStatistics(self) -> bool:
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
    m_totalEntitiesCreated = 0
    
    def __init__(self, name, numGen, entity : 'Entity', arrivalDist : 'Distribution'):
        super().__init__(name)
        
        self.m_type = self.Type.SOURCE
        
        self.m_numToGen = numGen
        self.m_entity = entity
        self.m_arrivalDist = arrivalDist
        self.m_infiniteGen = False
        
        # statistics handling
        self.sm_entitiesCreated = 0
        
        ScheduleEventIn(0.0, "Placeholder time unit", self.ArriveEA(self))
        pass    
    
    def Accept(self, visitor : 'Visitor'):
        return visitor.visit_source(self)
    
    def HasGraphableStatistics(self) -> bool:
        return False
    
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
        self.sm_entitiesCreated += 1
        
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
    
    ## static member variables
    sm_totalProcessed = 0
    sm_totalWaitTime = 0
    sm_totalIdleTime = 0
    
    class State(Enum):
        BUSY = 0
        IDLE = 1
    
    def __init__(self, name, serviceTime : 'Distribution'):
        super().__init__(name) 
        
        self.m_type = self.Type.SERVER  
        self.m_state = self.State.IDLE
        self.m_serviceDist = serviceTime
        self.m_queue = FIFO()
        
        ## statistics handling
        self.sm_numberProcessed = 0
        self.sm_waitTime = 0
        self.sm_totalServiceTime = 0
        self.sm_idleTime = 0        
        
        # graphing statistics
        self.gsm_event_times = [] # x
        self.gsm_state_trajectory = [] # y
        pass
    
    def Accept(self, visitor: Visitor):
        return visitor.visit_server(self)
    
    def HasGraphableStatistics(self) -> bool:
        return True
    
    def NodeProcess(self, entity: Entity) -> None:
        self.m_queue.AddEntity(entity)
        
        if self.m_state == self.State.IDLE:
            ScheduleEventIn(0.0, "Placeholder time unit", self.StartProcessingEA(self))
            pass
        pass
    
    def CleanupStatisticsLists(self):
        
        # go through the state trajectory and the event times and 
        # remove the state value and events that have multipl state values in a row
        # This is the make the graph look nicer, fully optional
        
        # trying to remove the spikes in the graph by removing the duplicate values
        
        two_states_back = self.gsm_state_trajectory[0]
        one_state_back = self.gsm_state_trajectory[1]
        current_state = self.gsm_state_trajectory[2]
        
        two_times_back = self.gsm_event_times[0]
        one_time_back = self.gsm_event_times[1]
        current_time = self.gsm_event_times[2]

        for time in self.gsm_event_times:
            
            if(iter < 3):
                iter += 1
                continue
            
            # need to check if each of the states is equal to each other 
            # AND if the time is the same too
            
            if(two_states_back == one_state_back and two_times_back == one_time_back):
                
                # remove the two states back and the two times back
                
                
                pass
            
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
        
        # check to see if there is a concrete state change
        # not just, done with entity grabbing a new one
        if(self.gsm_event_times.__len__() > 0):
            if(self.gsm_event_times[-1] == GetSimulationTime()
            and self.gsm_state_trajectory[-1] == self.gsm_state_trajectory[-2]):
                
                self.gsm_event_times.pop()
                self.gsm_state_trajectory.pop()            
                return          
            pass
        
        self.gsm_event_times.append(GetSimulationTime())
        self.gsm_state_trajectory.append(self.m_state.value)
        
        self.m_state = self.State.BUSY
        
        self.gsm_event_times.append(GetSimulationTime())
        self.gsm_state_trajectory.append(self.m_state.value)
        
        serviceTime = self.m_serviceDist.GetRV()
        
        entity : 'Entity'
        entity = self.m_queue.GetEntity()
        entity.sm_exitQueueTime = GetSimulationTime()
        entity.sm_waitTime = entity.sm_exitQueueTime - entity.sm_enterQueueTime
        
        self.sm_waitTime += entity.sm_waitTime
        self.sm_totalWaitTime += entity.sm_waitTime
        self.sm_totalServiceTime += serviceTime
        self.sm_time_utilized += serviceTime
        
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
        
        if(self.gsm_event_times.__len__() > 0):
            if(self.gsm_event_times[-1] == GetSimulationTime()
            and self.gsm_state_trajectory[-1] == self.m_state.value):
                
                self.gsm_event_times.pop()
                self.gsm_state_trajectory.pop()            
                return          
            pass
        
        self.gsm_event_times.append(GetSimulationTime())
        self.gsm_state_trajectory.append(self.m_state.value)
        
        self.m_state = self.State.IDLE
        
        self.gsm_event_times.append(GetSimulationTime())
        self.gsm_state_trajectory.append(self.m_state.value)
        
        self.sm_numberProcessed += 1
        self.sm_totalProcessed += 1
        
        if not self.m_queue.IsEmpty():
            ScheduleEventIn(0.0, "Placeholder time unit", self.StartProcessingEA(self))
            pass
        
        message = "Time: " + str(GetSimulationTime()) + "\tServer " + str(self.m_id) + "\tEnd Processing\n"
        print(message)
        
        self.Depart(entity)        
        pass
    pass

class Sink(SimulationObject):
    
    ## static member variables
    sm_totalEntitiesDestroyed = 0
    
    def __init__(self, name):
        super().__init__(name)
        
        self.m_type = self.Type.SINK   
        
        self.sm_entitiesDestroyed = 0
        pass
    
    def Accept(self, visitor: Visitor):
        return visitor.visit_sink(self)
    
    def HasGraphableStatistics(self) -> bool:
        return False
    
    def NodeProcess(self, entity: Entity) -> None:
        
        message = "Deleting " + str(entity.m_ID) + "\n"
        print(message)        
        
        entity.SetDeletionTime(GetSimulationTime())        
        
        self.sm_entitiesDestroyed += 1
        self.sm_totalEntitiesDestroyed += 1        
        pass    
    pass
