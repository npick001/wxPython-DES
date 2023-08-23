import wx

class GraphicalElement:
    SELECTION_STATE_NAMES = [
        "NONE",
		"NODE",
		"NODE_OUTPUT",
		"NODE_INPUT",
		"NODE_SIZER",
		"EDGE"]
    
    # static variables
    m_nextID = 1
    
    def __init__(self):
        self.m_id = GraphicalElement.m_nextID
        GraphicalElement.m_nextID = GraphicalElement.m_nextID + 1
        
        self.m_is_selected = False
        self.m_label = "Element " + str(self.m_id)        
        pass
    
    def __eq__(self, other : 'GraphicalElement') -> bool:
        return (self.m_id == other.m_id)
    
    def SetSelected(self, selected : bool):
        self.m_is_selected = selected
        pass
    
    def Select(self, camera : 'wx.AffineMatrix2D', clickPosition : 'wx.GraphicsContext'):
        # VIRTUAL FUNCTION TO BE OVERRIDDEN
        pass