import wx
import wx.aui
import numpy as np
import wx.lib.agw.aui as aui
import matplotlib.pyplot as plt
from GraphingPanels import HistogramPanel
from enum import Enum
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

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

        # Create a menu bar
        menubar = wx.MenuBar()

        ### CREATE MENUS
        # File menu
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN)
        file_menu.Append(wx.ID_SAVE)
        file_menu.Append(wx.ID_SAVEAS)
        file_menu.Append(wx.ID_EXIT, "Exit\tAlt-F4", "Exit the application.")
        # Edit menu
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_UNDO)
        edit_menu.Append(wx.ID_REDO)
        edit_menu.AppendSeparator()
        edit_menu.Append(wx.ID_CUT)
        edit_menu.Append(wx.ID_COPY)
        edit_menu.Append(wx.ID_PASTE)
        # View menu
        view_menu = wx.Menu()
        view_menu.Append(self.Enums.ID_CREATE_NOTEBOOK.value, "Create Notebook", "Notebooks hold Canvases, the basis for your simulation model.")
        view_menu.Append(self.Enums.ID_CREATE_CANVAS.value, "Create Canvas", "Create a new Canvas in the currently selected Notebook.")
        # Settings menu
        settings_menu = wx.Menu()
        settings_menu.Append(self.Enums.ID_MODEL_SETTINGS.value, "Model Settings", "Change Model Settings")
        # Project menu
        project_menu = wx.Menu()
        project_menu.Append(self.Enums.ID_BUILD.value, "Build", "Build simulation code for currently selected canvas")
        project_menu.Append(self.Enums.ID_RUN.value, "Run", "Run the built simulation code")
        project_menu.Append(self.Enums.ID_BUILD_AND_RUN.value, "Build and Run", "Build & Run simulation for currently selected canvas")
        # Statistics menu
        stats_menu = wx.Menu()
        stats_menu.Append(self.Enums.ID_INPUT_ANALYZER.value, "Input Analyzer")

        # Link menus to menubar
        menubar.Append(file_menu, "File")
        menubar.Append(edit_menu, "Edit")
        menubar.Append(view_menu, "View")
        menubar.Append(settings_menu, "Settings")
        menubar.Append(project_menu, "Project")
        menubar.Append(stats_menu, "Statistics")
        
        # Set menu bar for this frame
        self.SetMenuBar(menubar)
        self.panel = HistogramPanel(self)
        self.aui_manager.AddPane(self.panel, aui.AuiPaneInfo().Left)

        # Update the aui manager
        self.aui_manager.Update()
        
        ### EVENT BINDING
        # File Menu
        file_menu.Bind(wx.EVT_MENU, self.OnOpen)
        file_menu.Bind(wx.EVT_MENU, self.OnSave)
        file_menu.Bind(wx.EVT_MENU, self.OnSaveAs)
        file_menu.Bind(wx.EVT_MENU, self.OnExit)
        # Edit Menu
        edit_menu.Bind(wx.EVT_MENU, self.OnUndo)
        edit_menu.Bind(wx.EVT_MENU, self.OnRedo)
        edit_menu.Bind(wx.EVT_MENU, self.OnCut)
        edit_menu.Bind(wx.EVT_MENU, self.OnCopy)
        edit_menu.Bind(wx.EVT_MENU, self.OnPaste)
        # View Menu
        view_menu.Bind(wx.EVT_MENU, self.OnCreateNotebook)
        view_menu.Bind(wx.EVT_MENU, self.OnCreateCanvas)
        # Settings Menu
        settings_menu.Bind(wx.EVT_MENU, self.OnChangeModelSettings)
        # Project Menu
        project_menu.Bind(wx.EVT_MENU, self.OnBuild)
        project_menu.Bind(wx.EVT_MENU, self.OnRun)
        project_menu.Bind(wx.EVT_MENU, self.OnBuildAndRun)
        # Statistics Menu
        stats_menu.Bind(wx.EVT_MENU, self.OnClickAnalyzer)
    
    ### EVENT HANDLING
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
        