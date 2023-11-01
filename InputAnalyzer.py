import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class InputAnalyzer:
    def __init__(self) -> None:
        self.data = []
        self.num_bins = 20
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
            
            self.data.append(float(line))
            pass

        # print all the data showing that it was loaded correctly
        for i in range(len(self.data)):
            print(self.data[i])
            pass
        
        data_file.close()
        pass
    
    def Plot_Histogram(self):
        # plot the data
        plt.hist(self.data, bins=self.num_bins)
        plt.title('Sample Histogram')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.show()
        pass
    pass