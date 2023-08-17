from queue import PriorityQueue
import Entity
from enum import Enum

## SHOULD BE COMPLETED FOR NOW
## NO TESTING HAS BEEN DONE YET
## TEST WITH SIMULATION OBJECTS WHEN THATS DONE

class TimeUnit(Enum):
    SECONDS = 1
    MINUTES = 60
    HOURS = 360
    YEARS = 21600
    
class EventAction:
    def __init__(self) -> None:
        pass
    
    ## Virtual fn for executing event actions
    def Execute() -> None:
        pass  
        
### NOT WORKING MORE TESTED NEEDED
class SimulationExecutive:
    
    m_modelTimeUnit = TimeUnit.SECONDS
    m_simTime = 0
    m_events = PriorityQueue()
    
    class Event:
        def __init__(self, time, eventAction) -> None:
            self.m_time = time
            self.m_ea = eventAction
            pass
        def GetTime(self):
            return self.m_time
    
    @classmethod
    def GetSimulationTime(cls) -> float:
        return cls.m_simTime
    
    @classmethod
    def RunSimulation(cls):
        cls.m_simTime = 0
        
        while not cls.m_events.empty():
            
            ## get event with smallest time stamp
            thisEvent = cls.m_events.get()
            
            ## Value updating and execution            
            cls.m_simTime = thisEvent.m_time
            thisEvent.m_ea.Execute()            
            pass
        pass
    
    # @staticmethod
    # def RunSimulation(endTime):
    #     SimulationExecutive.m_simTime = 0
        
    #     while not SimulationExecutive.m_events.empty():

    #         ## get event with smallest time stamp
    #         thisEvent : SimulationExecutive.Event
    #         thisEvent = SimulationExecutive.m_events.get()
            
    #         ## Value updating and execution            
    #         SimulationExecutive.m_simTime = thisEvent.m_time
    #         if (SimulationExecutive.m_simTime <= endTime):
    #             thisEvent.m_ea.Execute()            
    #             pass
            
    #         pass
    #     pass
    
    @classmethod
    def ScheduleEventIn(cls, deltaTime, timeUnit : TimeUnit, ea):
        
        ## get correct absolute time
        ## later will need to do some time unit conversions
        eventTime = GetSimulationTime() + deltaTime
        event = cls.Event(eventTime, ea)
        cls.m_events.put((eventTime, event))
        pass
    
    @classmethod
    def ScheduleEventAt(cls, time, timeUnit : TimeUnit, ea):
        
        ## later will need to do some time unit conversions
        eventTime = time
        event = cls.Event(eventTime, ea)
        cls.m_events.put((eventTime, event))
        pass
    
            
def GetSimulationTime() -> float:
    return SimulationExecutive.GetSimulationTime()

def RunSimulation():
    SimulationExecutive.RunSimulation()
    
# def RunSimulation(endtime):
#     SimulationExecutive.RunSimulation(endtime)
    
def ScheduleEventIn(delta, unit, action):
    SimulationExecutive.ScheduleEventIn(delta, unit, action)
    
def ScheduleEventAt(time, unit, action):
    SimulationExecutive.ScheduleEventAt(time, unit, action)
   