from collections import deque
import Entity

## SimExec Functions
from SimulationExecutive import GetSimulationTime
from SimulationExecutive import RunSimulation
from SimulationExecutive import ScheduleEventIn
from SimulationExecutive import ScheduleEventAt

# FIFO Queue - First In/First Out
# This class only handles entities for a FIFO Queue scheme.
# This data structure provides built in functions for statistics collection.
    
## SHOULD BE COMPLETED FOR NOW

class FIFO:
    def __init__(self):
        
        ## initialize FIFO queue
        self.m_queue = deque()
        self.m_size = 0        
        
        ## stats stuff
        self.m_total = 0
        self.m_queueSizeMin = 0
        self.m_queueSizeMax = 0
        self.m_queueSizeSum = 0
        self.m_count = 0
        self.m_cdfWaits = 0       
        pass
    
    def AddEntity(self, entity : Entity):
        self.m_queue.append(entity)
        
        # stats handling
        if(self.m_queueSizeMax < self.m_size):
            self.m_queueSizeMax = self.m_size
            pass
        
        entity.EnterQueue(GetSimulationTime())
        m_size += 1
        pass
    
    def GetEntity(self) -> 'Entity':
        toReturn = self.m_queue.popleft()
        
        # stats handling
        if (self.m_queueSizeMin > self.m_size):
            self.m_queueSizeMin = self.m_size
            pass
        
        self.m_cdfWaits += toReturn.LeaveQueue(GetSimulationTime())
        self.m_queueSizeSum += self.m_size
        m_size -= 1
        return toReturn
    
    def ViewEntity(self) -> 'Entity':
        copiedEnt = self.m_queue.popleft()
        toReturn = copiedEnt
        self.m_queue.appendleft(copiedEnt)
        
        return toReturn
    
    def GetAverageWaitTime(self) -> float:
        return (self.m_cdfWaits / self.m_total)
    
    def GetAverageQueueSize(self) -> float:
        return (self.m_queueSizeSum / self.m_total)
    
    def GetMinimumQueueSize(self) -> float:
        return self.m_queueSizeMin
    
    def GetMaximumQueueSize(self) -> float:
        return self.m_queueSizeMax
    
    def IsEmpty(self) -> bool:
        return (self.m_size == 0)
    
    def GetSize(self) -> int:
        return self.m_size
    