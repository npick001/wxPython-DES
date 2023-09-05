import wx
import wx.propgrid as wxpg

class PropertiesViewer(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        width, height = self.GetClientSize()
        width *= 0.2
        panel_size = wx.Size(width, height)
        
        self.m_selected_node = None
        
        self.m_properties = []
        self.m_property_grid = wxpg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, panel_size, wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_BOLD_MODIFIED)
        
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wxpg.EVT_PG_CHANGED, self.OnDistributionChange)
        self.Bind(wxpg.EVT_PG_CHANGED, self.OnDistributionPropertyChange)
            
    def Reset(self):
        for property in self.m_properties:
            self.m_property_grid.RemoveProperty(property)
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
    def RemoveProperty(self, property):
        
        if property in self.m_properties:
            
            property : 'wxpg.PGProperty'
            property.DeleteChildren()
            
            self.m_property_grid.RemoveProperty(property)
            self.m_properties.remove(property)
            pass
        else:
            wx.LogMessage("Selected property to remove does not exist.")
            pass
        pass
    def ResetPropertyGrid(self):
        
        pass
    
    # EVENT HANDLING
    def OnResize(self, event):
        pass
    def OnDistributionChange(self, event):
        pass
    def OnDistributionPropertyChange(self, event):
        pass
    pass

