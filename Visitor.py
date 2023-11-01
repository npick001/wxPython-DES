import Utility
from SimulationObjects import Source, Server, Sink

## DEFINE THE VISITOR PATTERN INTERFACE
# need to visit each simulation object
class Visitor:
    def visit_source(self, source : 'Source'):
        pass
    
    def visit_server(self, server : 'Server'):
        pass
    
    def visit_sink(self, sink : 'Sink'):
        pass    
    pass

## IMPLEMENT THE VISITOR PATTERN INTERFACE
class StatisticsVisitor(Visitor):
    def visit_source(self, source : 'Source'):
        source_statistics = [
            ("Time Utilized", source.m_time_utilized),
            ("Time Starved", source.m_time_starved),
            ("Resource Utilization", source.m_resource_utilization),
            ("Entities Created", source.sm_entitiesCreated),
        ]
        
        return source_statistics
    
    def visit_server(self, server : 'Server'):
        server_statistics = [
            ("Time Utilized", server.m_time_utilized),
            ("Time Starved", server.m_time_starved),
            ("Resource Utilization", server.m_resource_utilization),
            ("Number Processed", server.sm_numberProcessed),
            ("Wait Time", server.sm_waitTime),
            ("Total Service Time", server.sm_totalServiceTime),
            ("Idle Time", server.sm_idleTime),
        ]
            
        return server_statistics
    
    def visit_sink(self, sink : 'Sink'):
        sink_statistics = [            
            ("Time Utilized", sink.m_time_utilized),
            ("Time Starved", sink.m_time_starved),
            ("Resource Utilization", sink.m_resource_utilization),
            ("Entities Destroyed", sink.sm_entitiesDestroyed),
        ]
        
        return sink_statistics        
    pass