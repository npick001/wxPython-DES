import wx
import Distributions
from Entity import Entity
from MainFrame import MainFrame
from SimulationObjects import Source, Server, Sink
from SimulationExecutive import GetSimulationTime, RunSimulation

## SHOULD BE COMPLETED FOR NOW

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame.GetInstance()
        self.frame.Show()
        return True
    pass

if __name__ == '__main__':    
    app = MyApp(False)
    app.MainLoop()
    pass