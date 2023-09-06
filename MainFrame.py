import wx
import wx.aui
import numpy as np
import matplotlib.pyplot as plt
import Canvas
from PropertiesViewer import PropertiesViewer 
from enum import Enum
from SimProject import SimulationProject
from GraphingPanels import HistogramPanel

class MainFrame(wx.Frame):
    class Enums(Enum):
        ID_CREATE_NOTEBOOK = 990
        ID_CREATE_CANVAS = 991
        ID_MODEL_SETTINGS = 992
        ID_INPUT_ANALYZER = 993
        ID_BUILD = 994
        ID_RUN = 995
        ID_BUILD_AND_RUN = 996
    
    # static variables
    _instance = None
    
    @classmethod
    def GetInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
            pass
        return cls._instance
    
    # this is essentially the constructor
    def __init__(self):
        super(MainFrame, self).__init__(None, title="Python Discrete Simulator", size=(800, 600))
        
        # Initialize the AUI manager
        self.m_aui_manager = wx.aui.AuiManager(self)
        self.Maximize(True)

        # Create a menu bar
        self.m_menubar = wx.MenuBar()
        
        self.m_status_bar_fields = 4
        self.m_debug_status_bar = self.CreateStatusBar()
        self.m_debug_status_bar.SetFieldsCount(self.m_status_bar_fields)

        ### CREATE MENUS
        # File menu
        self.m_file_menu = wx.Menu()
        self.m_file_menu.Append(wx.ID_OPEN)
        self.m_file_menu.Append(wx.ID_SAVE)
        self.m_file_menu.Append(wx.ID_SAVEAS)
        self.m_file_menu.Append(wx.ID_EXIT, "Exit\tAlt-F4", "Exit the application.")
        # Edit menu
        self.m_edit_menu = wx.Menu()
        self.m_edit_menu.Append(wx.ID_UNDO)
        self.m_edit_menu.Append(wx.ID_REDO)
        self.m_edit_menu.AppendSeparator()
        self.m_edit_menu.Append(wx.ID_CUT)
        self.m_edit_menu.Append(wx.ID_COPY)
        self.m_edit_menu.Append(wx.ID_PASTE)
        # View menu
        self.m_view_menu = wx.Menu()
        self.m_view_menu.Append(self.Enums.ID_CREATE_NOTEBOOK.value, "Create Notebook", "Notebooks hold Canvases, the basis for your simulation model.")
        self.m_view_menu.Append(self.Enums.ID_CREATE_CANVAS.value, "Create Canvas", "Create a new Canvas in the currently selected Notebook.")
        # Settings menu
        self.m_settings_menu = wx.Menu()
        self.m_settings_menu.Append(self.Enums.ID_MODEL_SETTINGS.value, "Model Settings", "Change Model Settings")
        # Project menu
        self.m_project_menu = wx.Menu()
        self.m_project_menu.Append(self.Enums.ID_BUILD.value, "Build", "Build simulation code for currently selected canvas")
        self.m_project_menu.Append(self.Enums.ID_RUN.value, "Run", "Run the built simulation code")
        self.m_project_menu.Append(self.Enums.ID_BUILD_AND_RUN.value, "Build and Run", "Build & Run simulation for currently selected canvas")
        # Statistics menu
        self.m_stats_menu = wx.Menu()
        self.m_stats_menu.Append(self.Enums.ID_INPUT_ANALYZER.value, "Input Analyzer")

        # Link menus to menubar
        self.m_menubar.Append(self.m_file_menu, "File")
        self.m_menubar.Append(self.m_edit_menu, "Edit")
        self.m_menubar.Append(self.m_view_menu, "View")
        self.m_menubar.Append(self.m_settings_menu, "Settings")
        self.m_menubar.Append(self.m_project_menu, "Project")
        self.m_menubar.Append(self.m_stats_menu, "Statistics")
        
        # Set menu bar for this frame
        self.SetMenuBar(self.m_menubar)
        
        # generate the canvas
        self.m_canvas = Canvas.Canvas(self, self.m_debug_status_bar)
        self.m_canvas.m_mainframe_reference = self
        self.m_aui_manager.AddPane(self.m_canvas, wx.aui.AuiPaneInfo().CenterPane().Dockable(True))
        self.m_canvas.InitializeOriginLocation(self.GetSize())
        
        # simulation project
        self.m_simulation_project = SimulationProject()
        self.m_simulation_project.SetCanvas(self.m_canvas)
        
        # properties viewer
        self.m_properties_viewer = PropertiesViewer(self)
        self.m_properties_viewer.SetSize(self.GetSize())
        self.m_aui_manager.AddPane(self.m_properties_viewer, wx.aui.AuiPaneInfo().Right().Dockable(True).Resizable(True))
        
        # Update the aui manager
        self.m_aui_manager.Update()
        
        ### EVENT BINDING
        # Basic Panel Events
        self.Bind(wx.EVT_SIZE, self.OnResize)      
        # File Menu
        self.m_file_menu.Bind(wx.EVT_MENU, self.OnOpen)
        self.m_file_menu.Bind(wx.EVT_MENU, self.OnSave)
        self.m_file_menu.Bind(wx.EVT_MENU, self.OnSaveAs)
        self.m_file_menu.Bind(wx.EVT_MENU, self.OnExit)
        # Edit Menu
        self.m_edit_menu.Bind(wx.EVT_MENU, self.OnUndo)
        self.m_edit_menu.Bind(wx.EVT_MENU, self.OnRedo)
        self.m_edit_menu.Bind(wx.EVT_MENU, self.OnCut)
        self.m_edit_menu.Bind(wx.EVT_MENU, self.OnCopy)
        self.m_edit_menu.Bind(wx.EVT_MENU, self.OnPaste)
        # View Menu
        self.m_view_menu.Bind(wx.EVT_MENU, self.OnCreateNotebook, id=self.Enums.ID_CREATE_NOTEBOOK.value)
        self.m_view_menu.Bind(wx.EVT_MENU, self.OnCreateCanvas, id=self.Enums.ID_CREATE_CANVAS.value)
        # Settings Menu
        self.m_settings_menu.Bind(wx.EVT_MENU, self.OnChangeModelSettings, id=self.Enums.ID_MODEL_SETTINGS.value)
        # Project Menu
        self.m_project_menu.Bind(wx.EVT_MENU, self.OnBuild, id=self.Enums.ID_BUILD.value)
        self.m_project_menu.Bind(wx.EVT_MENU, self.OnRun, id=self.Enums.ID_RUN.value)
        self.m_project_menu.Bind(wx.EVT_MENU, self.OnBuildAndRun, id=self.Enums.ID_BUILD_AND_RUN.value)
        # Statistics Menu
        self.m_stats_menu.Bind(wx.EVT_MENU, self.OnClickAnalyzer, id=self.Enums.ID_INPUT_ANALYZER.value)
    
    def RegisterNewSelection(self, new_selection):
        
        self.m_properties_viewer.Reset()
        selection_properties = new_selection.GetProperties()
        
        for property in selection_properties:
            self.m_properties_viewer.AddProperty(property)
            pass
        
        self.m_properties_viewer.SetSelectedObject(new_selection)
        self.m_properties_viewer.Refresh()        
        pass
    
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
        self.m_simulation_project.Build()
        self.m_simulation_project.CheckBuildViability()
        pass
    
    def OnRun(self, event):
        self.m_simulation_project.Run()
        pass
    
    def OnBuildAndRun(self, event):
        
        if self.m_simulation_project.HasBeenBuilt():
            
            self.m_simulation_project.Run()
            pass
        else:
            wx.MessageBox("You must build the project before running it.", "Error", wx.OK | wx.ICON_ERROR)
            pass
        pass
        