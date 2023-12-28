import wx
import math
from GraphingPanels import *

class InputAnalyzer(wx.Panel):
    def __init__(self, parent) -> None:
        super(InputAnalyzer, self).__init__(parent)
        self.m_data = []
        self.m_num_bins = 20
        hist_size = wx.Size(400, 300)
        self.m_histogram = HistogramPanel(self, hist_size, self.m_num_bins)  # Adjust size as needed
                
        self.m_data_input_button = wx.Button(self, label="Load Data")
        self.m_data_input_button.Bind(wx.EVT_BUTTON, self.on_button_click)  # Add event binding for button click
        
        self.m_color_choices = ["Red", "Blue", "Green", "Black", "Yellow", "Cyan"]
        self.m_color_change_dropdown = wx.ComboBox(self, value="Blue", choices=self.m_color_choices, style=wx.CB_READONLY)
        self.m_color_change_dropdown.Bind(wx.EVT_COMBOBOX, self.on_color_change)

        self.m_sizer = wx.BoxSizer(wx.HORIZONTAL)        
        self.SetBackgroundColour(wx.WHITE)
        self.AddComponents()
        self.SetSizer(self.m_sizer)
        pass
    
    def AddComponents(self):
        # Button sizer for positioning the button
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer.AddStretchSpacer(prop=2)
        
        # # Dropdown for color selection
        # self.color_choice = wx.Choice(self, choices=self.m_color_choices)
        # self.color_choice.Bind(wx.EVT_CHOICE, self.on_color_change)
        
        # Add button to the button sizer
        button_sizer.Add(self.m_data_input_button, 0, wx.SHAPED, wx.ALIGN_CENTER)
        button_sizer.Add(self.m_color_change_dropdown, 0, wx.SHAPED, wx.ALIGN_CENTER)
        button_sizer.AddStretchSpacer(prop=4)

        # Add button sizer and histogram panel to the main sizer
        self.m_sizer.Add(button_sizer, 1, wx.EXPAND | wx.ALL, 25)  # Adjust proportion and border as needed
        self.m_sizer.Add(self.m_histogram, 2, wx.EXPAND | wx.ALL, 10)  # Adjust proportion and border as needed       
        pass
    
    def ReadFile(self, filename):
        # open the file
        data_file = open(filename, 'r', encoding='utf-8')
        
        num_lines = data_file.readline()
        
        # read all the data from the file
        while(True):
            line = data_file.readline()

            # if the line is empty, we have reached the end of the file
            if not line:
                break
            
            self.m_data.append(float(line))
            pass

        # print all the data showing that it was loaded correctly
        # for i in range(len(self.data)):
        #     print(self.data[i])
        #     pass
        
        data_file.close()
        pass
    
    def Plot_Histogram(self):
        # plot the data
        self.m_histogram.m_data = self.m_data
        self.m_histogram.m_num_bins = int(math.sqrt(len(self.m_data)))
        self.m_histogram.set_color(self.m_color_change_dropdown.GetValue())
        self.m_histogram.draw_graph()
        pass
    
    def on_button_click(self, event):
        # Open file dialog to select file
        with wx.FileDialog(self, "Open data file", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.ReadFile(pathname)
            self.Plot_Histogram()
            pass            
        pass
    
    def on_color_change(self, event):
        selected_color = self.m_color_change_dropdown.GetValue()
        self.m_histogram.set_color(selected_color)
        pass
    pass