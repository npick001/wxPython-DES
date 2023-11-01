import Utility
from SimulationExecutive import GetSimulationTime

## DEFINE THE VISITOR PATTERN INTERFACE
# need to visit each simulation object
class Visitor:
    def visit_source(self, source : 'Source'):
        pass
    
    def visit_server(self, server : 'Server'):
        pass
    
    def visit_sink(self, sink : 'Sink'):
        pass    
    
    def visit_entity(self, entity : 'Entity'):
        pass
    pass

## IMPLEMENT THE VISITOR PATTERN INTERFACE
class StatisticsVisitor(Visitor):
    def visit_source(self, source):
        source_statistics = [
            ("Entities Created", source.sm_entitiesCreated),
        ]
        
        return source_statistics
    
    def visit_server(self, server):
        
        # calculate time starved and resource utilization
        time_utilized = float(server.sm_time_utilized)
        time_starved = GetSimulationTime() - time_utilized
        percent_util = server.sm_time_utilized / GetSimulationTime()
        
        server_statistics = [
            ("Time Utilized", server.sm_time_utilized),
            ("Time Starved", time_starved),
            ("Resource Utilization", percent_util),
            ("Number Processed", server.sm_numberProcessed),
            ("Wait Time", server.sm_waitTime),
            ("Total Service Time", server.sm_totalServiceTime),
        ]
            
        return server_statistics
    
    def visit_sink(self, sink):
        sink_statistics = [            
            ("Entities Destroyed", sink.sm_entitiesDestroyed),
        ]
        
        return sink_statistics           
    pass