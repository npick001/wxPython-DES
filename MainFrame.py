import wx
import wx.aui
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from GraphingPanels import HistogramPanel
import Canvas

class MainFrame(wx.Frame):
    class Enums(Enum):
        ID_CREATE_NOTEBOOK = 990
        ID_CREATE_CANVAS = 991
        ID_MODEL_SETTINGS = 992
        ID_INPUT_ANALYZER = 993
        ID_BUILD = 994
        ID_RUN = 995
        ID_BUILD_AND_RUN = 996
    
    # this is essentially the constructor
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        
        # Initialize the AUI manager
        self.aui_manager = wx.aui.AuiManager(self)
        self.Maximize(True)

        # Create a menu bar
        self.menubar = wx.MenuBar()
        
        self.m_status_bar_fields = 4
        self.m_debug_status_bar = self.CreateStatusBar()
        self.m_debug_status_bar.SetFieldsCount(self.m_status_bar_fields)

        ### CREATE MENUS
        # File menu
        self.file_menu = wx.Menu()
        self.file_menu.Append(wx.ID_OPEN)
        self.file_menu.Append(wx.ID_SAVE)
        self.file_menu.Append(wx.ID_SAVEAS)
        self.file_menu.Append(wx.ID_EXIT, "Exit\tAlt-F4", "Exit the application.")
        # Edit menu
        self.edit_menu = wx.Menu()
        self.edit_menu.Append(wx.ID_UNDO)
        self.edit_menu.Append(wx.ID_REDO)
        self.edit_menu.AppendSeparator()
        self.edit_menu.Append(wx.ID_CUT)
        self.edit_menu.Append(wx.ID_COPY)
        self.edit_menu.Append(wx.ID_PASTE)
        # View menu
        self.view_menu = wx.Menu()
        self.view_menu.Append(self.Enums.ID_CREATE_NOTEBOOK.value, "Create Notebook", "Notebooks hold Canvases, the basis for your simulation model.")
        self.view_menu.Append(self.Enums.ID_CREATE_CANVAS.value, "Create Canvas", "Create a new Canvas in the currently selected Notebook.")
        # Settings menu
        self.settings_menu = wx.Menu()
        self.settings_menu.Append(self.Enums.ID_MODEL_SETTINGS.value, "Model Settings", "Change Model Settings")
        # Project menu
        self.project_menu = wx.Menu()
        self.project_menu.Append(self.Enums.ID_BUILD.value, "Build", "Build simulation code for currently selected canvas")
        self.project_menu.Append(self.Enums.ID_RUN.value, "Run", "Run the built simulation code")
        self.project_menu.Append(self.Enums.ID_BUILD_AND_RUN.value, "Build and Run", "Build & Run simulation for currently selected canvas")
        # Statistics menu
        self.stats_menu = wx.Menu()
        self.stats_menu.Append(self.Enums.ID_INPUT_ANALYZER.value, "Input Analyzer")

        # Link menus to menubar
        self.menubar.Append(self.file_menu, "File")
        self.menubar.Append(self.edit_menu, "Edit")
        self.menubar.Append(self.view_menu, "View")
        self.menubar.Append(self.settings_menu, "Settings")
        self.menubar.Append(self.project_menu, "Project")
        self.menubar.Append(self.stats_menu, "Statistics")
        
        # Set menu bar for this frame
        self.SetMenuBar(self.menubar)
        self.panel = Canvas.Canvas(self, self.m_debug_status_bar)
        self.aui_manager.AddPane(self.panel, wx.aui.AuiPaneInfo().CenterPane().Dockable(True))
        self.panel.InitializeOriginLocation(self.GetSize())
        
        # Update the aui manager
        self.aui_manager.Update()
        
        ### EVENT BINDING
        # Basic Panel Events
        self.Bind(wx.EVT_SIZE, self.OnResize)      
        # File Menu
        self.file_menu.Bind(wx.EVT_MENU, self.OnOpen)
        self.file_menu.Bind(wx.EVT_MENU, self.OnSave)
        self.file_menu.Bind(wx.EVT_MENU, self.OnSaveAs)
        self.file_menu.Bind(wx.EVT_MENU, self.OnExit)
        # Edit Menu
        self.edit_menu.Bind(wx.EVT_MENU, self.OnUndo)
        self.edit_menu.Bind(wx.EVT_MENU, self.OnRedo)
        self.edit_menu.Bind(wx.EVT_MENU, self.OnCut)
        self.edit_menu.Bind(wx.EVT_MENU, self.OnCopy)
        self.edit_menu.Bind(wx.EVT_MENU, self.OnPaste)
        # View Menu
        self.view_menu.Bind(wx.EVT_MENU, self.OnCreateNotebook)
        self.view_menu.Bind(wx.EVT_MENU, self.OnCreateCanvas)
        # Settings Menu
        self.settings_menu.Bind(wx.EVT_MENU, self.OnChangeModelSettings)
        # Project Menu
        self.project_menu.Bind(wx.EVT_MENU, self.OnBuild)
        self.project_menu.Bind(wx.EVT_MENU, self.OnRun)
        self.project_menu.Bind(wx.EVT_MENU, self.OnBuildAndRun)
        # Statistics Menu
        self.stats_menu.Bind(wx.EVT_MENU, self.OnClickAnalyzer)
    
    ### EVENT HANDLING
    
    def OnResize(self, event : 'wx.SizeEvent'):
        self.Refresh()
        pass
    
    # Essentially the deconstructor
    def OnExit(self, event):
        self.Close()
            
    def OnOpen(self, event):
        ## handle opening file
        wildcard = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
        
        dialog = wx.FileDialog(
            self,
            message="Choose a file",
            defaultDir="",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            selected_path = dialog.GetPath()
            print("Selected file:", selected_path)
        
        dialog.Destroy()
   
    def OnSave(self, event):
        ## handle saving file
        wildcard = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
        
        dialog = wx.FileDialog(
            self,
            message="Save file",
            defaultDir="",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            selected_path = dialog.GetPath()
            print("Saved file:", selected_path)
        
        dialog.Destroy()
        
    def OnSaveAs(self, event):        
        ## handle saving file
        wildcard = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
        
        dialog = wx.FileDialog(
            self,
            message="Save file",
            defaultDir="",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            selected_path = dialog.GetPath()
            print("Saved file as:", selected_path)
        
        dialog.Destroy()
        
    def OnCreateNotebook(self, event):
        return 0
    
    def OnCreateCanvas(self, event):
        return 0
        
    def OnClickAnalyzer(self, event):
        return 0
    
    def OnUndo(self, event):
        return 0
    
    def OnRedo(self, event):
        return 0
    
    def OnCut(self, event):
        return 0
    
    def OnCopy(self, event):
        return 0
    
    def OnPaste(self, event):
        return 0
    
    def OnChangeModelSettings(self, event):
        return 0
    
    def OnBuild(self, event):
        return 0
    
    def OnRun(self, event):
        return 0
    
    def OnBuildAndRun(self, event):
        return 0
        