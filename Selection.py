from enum import IntEnum
#from GraphicalElement import GraphicalElement

# ASSUMES THAT GRAPHICALEDGE IS DEFINED FIRST, WHICH IT SHOULD BE
# IMPORT PRIORITY ALWAYS POPULATES UPWARDS
# MORE IMPORTANT MODULES WILL IMPORT LESS IMPORTANT TO AVOID
# CIRCULAR IMPORTS
#
# i.e.: 
# - Graphical Node import GEdge and GElement
# -- GraphicalElement import Selection

class Selection:
    class State(IntEnum):
        NONE = 0
        NODE = 1
        NODE_OUTPUT = 2
        NODE_INPUT = 3
        NODE_ROTATOR = 4
        NODE_SIZER = 5
        EDGE = 6
        STATES_MAX = 7
        
    def __init__(self):
        self.m_element = None
        self.m_state = Selection.State.NONE
        pass
    
    def __eq__(self, other : 'Selection') -> bool:
        if(other == None):
            return False
        
        return self.m_element == other.m_element and self.m_state == other.m_state
    
    def __bool__(self) -> bool:
        return self.m_element != None
    
    def Reset(self):
        self.m_element = None
        self.m_state = self.State.NONE
        pass