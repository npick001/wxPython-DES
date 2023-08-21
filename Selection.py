from enum import Enum
from GraphicalElement import GraphicalElement

class Selection:
    class State(Enum):
        NONE = 9990
        NODE = 9991
        NODE_OUTPUT = 9992
        NODE_INPUT = 9993
        NODE_SIZER = 9994
        EDGE = 9995
        STATES_MAX = 6
        
    def __init__(self):
        self.m_element = GraphicalElement()
        self.m_state = self.State.NONE
        pass
    
    def Reset(self):
        self.m_element = GraphicalElement()
        self.m_state = self.State.NONE
        pass