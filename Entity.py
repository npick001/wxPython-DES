from enum import Enum
from SimulationExecutive import GetSimulationTime

## SHOULD BE COMPLETED FOR NOW

class Entity:
    class EntityType(Enum):
        ENTITY = "Entity"
        TRANSPORT = "Transport"
        BATCH = "Batch"
   
    # static class members
    m_nextID : int
        
    def __init__(self, creationTime : float):
        self.m_creationTime = creationTime
        
        self.m_nextID = 0
        self.m_ID = self.m_nextID + 1
        self.m_sourceID = -1
        
        self.m_nextID += 1
        pass
    
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
        pass
    def LeaveQueue(self, timeNow : float):
        pass