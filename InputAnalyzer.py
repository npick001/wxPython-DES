import wx
import math
import scipy as stats
from GraphingPanels import *
from Distributions import *

class InputAnalyzer(wx.Panel):
    def __init__(self, parent) -> None:
        super(InputAnalyzer, self).__init__(parent)
        self.m_data = list(np.random.uniform(0, 1, 1000))
        self.m_num_bins = 20
        hist_size = wx.Size(400, 300)
        self.m_histogram = HistogramPanel(self, hist_size, self.m_num_bins, data=self.m_data)  # Adjust size as needed
        
        # read only header text control for telling the user what this panel is for
        # should be a bit larger than the other controls and be centered on the left side of the panel
        self.m_header_text = wx.StaticText(self, label="Distribution Parameter Estimator")
        self.m_header_text.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # read only text control for telling the user what this panel is for
        # should be directly below the header text and be centered on the left side of the panel
        self.m_description_text = wx.StaticText(self, label="This panel is for estimating the distribution of input data.")
        self.m_description_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        # read only text control for telling the user what the fields below are used for
        # should be directly below the analyze button and be centered on the left side of the panel
        data_input_label = "Input data can be loaded from a file or entered manually. \n"
        data_input_label = data_input_label + "The first line of the file should be the number of data points, with every line after that containing a data point. \n"
        data_input_label = data_input_label + "The data should be in a single column with no headers or other information. \n"
        self.m_data_input_text = wx.StaticText(self, label=data_input_label)
        self.m_data_input_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        # Button for reading from a file
        self.m_data_input_button = wx.Button(self, label="Load Data From File")
        self.m_data_input_button.Bind(wx.EVT_BUTTON, self.on_click_readfile_button)
        
        # Dropdown for color selection
        self.m_color_choices = ["Red", "Blue", "Green", "Black", "Yellow", "Cyan"]
        self.m_color_change_dropdown = wx.ComboBox(self, value="Blue", choices=self.m_color_choices, style=wx.CB_READONLY)
        self.m_color_change_dropdown.Bind(wx.EVT_COMBOBOX, self.on_color_change)

        # Slider for number of bins
        self.bin_slider = wx.Slider(self, value=20, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL)
        self.bin_slider.Bind(wx.EVT_SLIDER, self.on_bin_slider_change)

        # TextCtrl for manual bin input
        self.bin_input = wx.TextCtrl(self, value="20", style=wx.TE_PROCESS_ENTER)
        self.bin_input.Bind(wx.EVT_TEXT_ENTER, self.on_bin_change)
        
        # create a large button for Analyzing data
        # should be centered on the left side of the panel
        self.m_analyze_button = wx.Button(self, label="\n\tEstimate Distribution\t\n\n")
        self.m_analyze_button.Bind(wx.EVT_BUTTON, self.on_click_analyze_button)

        # create an empty text control for displaying the results of the analysis
        # should be centered on the left side of the panel
        self.m_analysis_results_text = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.m_analysis_results_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        self.m_sizer = wx.BoxSizer(wx.HORIZONTAL)        
        self.SetBackgroundColour(wx.WHITE)
        self.AddComponents()
        self.SetSizer(self.m_sizer)
        pass
    
    def AddComponents(self):
        # Sizer for positioning the left side of the panel
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add static texts at the top with alignment and padding
        left_sizer.Add(self.m_header_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        left_sizer.Add(self.m_description_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)

        # Add other components with some vertical space between them
        left_sizer.Add(self.m_data_input_text, 0, wx.ALIGN_LEFT | wx.BOTTOM, 10)
        left_sizer.Add(self.m_data_input_button, 0, wx.SHAPED | wx.ALIGN_LEFT | wx.BOTTOM, 10)
        left_sizer.Add(self.m_color_change_dropdown, 0, wx.SHAPED | wx.ALIGN_LEFT | wx.BOTTOM, 10)
        left_sizer.Add(self.bin_input, 0, wx.EXPAND | wx.BOTTOM, 10)       
        left_sizer.Add(self.bin_slider, 0, wx.EXPAND | wx.BOTTOM, 10)
        left_sizer.Add(self.m_analyze_button, 0, wx.SHAPED | wx.ALIGN_CENTER | wx.BOTTOM, 20)
        left_sizer.Add(self.m_analysis_results_text, 1, wx.EXPAND | wx.BOTTOM, 10)

        # Add the histogram panel to the main sizer
        self.m_sizer.Add(left_sizer, 1, wx.EXPAND | wx.ALL, 25)
        self.m_sizer.Add(self.m_histogram, 2, wx.EXPAND | wx.ALL, 10)     
        pass
        
    def ReadFile(self, filename):
        self.m_data.clear()
        
        # open the file
        data_file = open(filename, 'r', encoding='utf-8')
        
        # read the number of lines, 
        # not exactly required for this version of the software
        num_lines = data_file.readline()
        
        # read all the data from the file
        while(True):
            line = data_file.readline()

            # if the line is empty, we have reached the end of the file
            if not line:
                break
            
            self.m_data.append(float(line))
            pass
        
        data_file.close()
        pass
    
    def Plot_Histogram(self):
        # plot the data
        self.m_histogram.m_data = self.m_data
        self.m_histogram.m_num_bins = int(math.sqrt(len(self.m_data)))
        self.m_histogram.set_color(self.m_color_change_dropdown.GetValue())
        self.m_histogram.draw_graph()
        pass
    
    def Analyze_Data(self):
        # List of distribution classes to test
        distributions = [
            Exponential(),
            Uniform(),
            Triangular(),
            Normal(),
            Weibull()
        ]

        best_fit_distribution = None
        best_fit_params = []
        best_fit_statistic = float('inf')
        ks_statistics = []

        # Fit data to each distribution and calculate goodness-of-fit
        for dist in distributions:
            dist : 'Distribution'
            params = dist.m_distribution.fit(self.m_data)
            statistic, p_value = stats.kstest(self.m_data, dist.m_distribution.name, args=params)

            # Update best fit if this distribution is a better fit
            if statistic < best_fit_statistic:
                ks_statistics.clear()
                ks_statistics.append(statistic)
                ks_statistics.append(p_value)
                
                best_fit_params = params
                best_fit_statistic = statistic
                best_fit_distribution = dist
                pass
            pass

        # Display or return the best fit distribution and its parameters
        if best_fit_distribution is not None:
            best_fit_distribution : 'Distribution'
            self.m_analysis_results_text.Clear()
            
            # Method of Moments Estimation
            # Assuming the 'fit' method of each distribution returns the estimated parameters
            self.m_analysis_results_text.AppendText(f"Best fit distribution: {best_fit_distribution.m_type.value}\n")
            self.m_analysis_results_text.AppendText(f"Estimated Parameters (Method of Moments): {best_fit_params}\n")
            
            # Kolmogorov-Smirnov Test
            # Assuming the 'fit' method of each distribution returns the estimated parameters
            
            self.m_analysis_results_text.AppendText(f"Kolmogorov-Smirnov Test Statistic: {ks_statistics[0]}\n")
            self.m_analysis_results_text.AppendText(f"Kolmogorov-Smirnov Test P-Value: {ks_statistics[1]}\n")
        
            # Update Histogram Panel
            self.m_histogram.set_theoretical_distribution(params, best_fit_distribution.m_type.value)
            pass
        else:
            print("No suitable distribution found.")
            pass
            
        self.m_histogram.set_theoretical_distribution(best_fit_distribution.m_distribution.fit(self.m_data), best_fit_distribution.m_type)  
        pass
    
    def on_click_readfile_button(self, event):
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
    
    def on_click_analyze_button(self, event):
        self.Analyze_Data()
        pass
    
    def on_color_change(self, event):
        selected_color = self.m_color_change_dropdown.GetValue()
        self.m_histogram.set_color(selected_color)
        pass
    
    def on_bin_slider_change(self, event):
        num_bins = self.bin_slider.GetValue()
        self.bin_input.SetValue(str(num_bins))
        self.m_histogram.set_num_bins(num_bins)
        pass
    
    def on_bin_change(self, event):
        num_bins = self.bin_input.GetValue()
        self.bin_slider.SetValue(int(num_bins))
        self.m_histogram.set_num_bins(int(num_bins))
        pass
    pass