from enum import Enum
from SimulationExecutive import GetSimulationTime

## SHOULD BE COMPLETED FOR NOW

class Entity:
    class EntityType(Enum):
        ENTITY = "Entity"
        TRANSPORT = "Transport"
        BATCH = "Batch"
   
    # static class members
    m_nextID = 0
        
    def __init__(self, creationTime : float):
        self.m_creationTime = creationTime
        
        self.m_ID = Entity.m_nextID
        self.m_sourceID = -1
        
        ## statitics
        self.sm_waitTime = 0
        self.sm_enterQueueTime = 0
        self.sm_exitQueueTime = 0
        self.sm_totalWaitTime = 0
        self.sm_numTimesStopped = 0        
        
        Entity.m_nextID += 1
        pass
    
    def Accept(self, visitor : 'Visitor'):
        return visitor.visit_entity(self)
    
    @classmethod
    def New(cls) -> 'Entity':
        return cls(GetSimulationTime())
    
    def SetSource(self, sourceID):
        self.m_sourceID = sourceID
    def SetType(self, type):
        self.m_type = type   
    def SetDeletionTime(self, timeNow : float):
        self.m_deletionTime = timeNow
    
    # stats stamping fns
    def EnterQueue(self, timeNow : float):
        self.m_enterQueue = timeNow
        pass
    def LeaveQueue(self, timeNow : float):
        self.m_leaveQueue = timeNow
        self.waitTime = self.m_leaveQueue - self.m_enterQueue
        return self.waitTime