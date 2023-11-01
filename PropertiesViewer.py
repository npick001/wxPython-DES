import wx
import wx.propgrid as wxpg

class PropertiesViewer(wx.Panel):
    
    def __init__(self, parent : 'wx.Window'):
        super(wx.Panel, self).__init__(parent)
        
        self.m_selected_node = None
        #self.m_main_frame = MainFrame(parent=None, title="Python Discrete Simulator")
        
        self.m_properties = []
        self.m_property_grid = wxpg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, self.GetSize(), wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_BOLD_MODIFIED)
        width, height = parent.GetSize()
        #width *= 0.2
        self.SetSize(wx.Size(width, height))
        
        self.header_property = wxpg.StringProperty("Property", wxpg.PG_LABEL, "Value")
        self.m_property_grid.Append(self.header_property)
        
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wxpg.EVT_PG_CHANGED, self.OnDistributionChange)
        self.Bind(wxpg.EVT_PG_CHANGED, self.OnDistributionPropertyChange)
            
    def Reset(self):       
        # iteratively remove all properties except the header
        for i in range(1, len(self.m_properties)):
            self.m_property_grid.RemoveProperty(self.m_properties[i])
            pass
        pass
    def Refresh(self):
        self.m_property_grid.Refresh()
        self.m_property_grid.Update()
        pass
    def SetSize(self, size):
        width = size.x 
        height = size.y
        new_size = wx.Size(width, height)
        
        self.m_property_grid.SetSize(new_size)
        self.Refresh()        
        pass
        
    def SetSelectedObject(self, obj):
        self.m_selected_node = obj
        pass
    def AddProperty(self, property):
        
        self.m_property_grid.Append(property)
        self.m_properties.append(property)
        
        self.Refresh()        
        pass
    def EditProperty(self, property : 'wxpg.PGProperty', new_value):
        
        property_changed = False
        for prop in self.m_properties:

            prop : 'wxpg.PGProperty'
            if prop.GetName() == property.GetName():
                prop.SetValue(new_value)
                property_changed = True
                break
            pass
        
        if not property_changed:
            wx.LogMessage("Selected property to edit does not exist.")
            pass
        pass
    def RemoveProperty(self, property : 'wxpg.PGProperty'):
        
        if property in self.m_properties:
            
            property.DeleteChildren()
            
            self.m_property_grid.RemoveProperty(property)
            self.m_properties.remove(property)
            pass
        else:
            wx.LogMessage("Selected property to remove does not exist.")
            pass
        pass
    def ResetPropertyGrid(self):
        
        for prop in self.m_properties:
            prop : 'wxpg.PGProperty'
            prop.DeleteChildren()
            self.m_property_grid.RemoveProperty(prop)
            pass        
        pass
    
    # EVENT HANDLING
    def OnResize(self, event):
        
        width = self.GetSize().x
        height = self.GetSize().y
        new_size = wx.Size(width, height)
        
        self.m_property_grid.SetSize(new_size)
        self.Refresh()        
        pass
    def OnDistributionChange(self, event):
        pass
    def OnDistributionPropertyChange(self, event):
        pass
    pass

