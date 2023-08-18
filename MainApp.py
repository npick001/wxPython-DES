import wx
import Distributions
from Entity import Entity
from MainFrame import MainFrame
from SimulationObjects import Source, Server, Sink

from SimulationExecutive import GetSimulationTime, RunSimulation

## SHOULD BE COMPLETED FOR NOW

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(parent=None, title="Separate Frame Example")
        self.frame.Show()
        return True

if __name__ == '__main__':
    # app = MyApp(False)
    # app.MainLoop()
    
    src = Source("Source", 10, Entity(GetSimulationTime()), Distributions.Exponential(1))
    server = Server("Server", Distributions.Triangular(1, 2, 3))
    sink = Sink("Sink")
    
    src.AddNext(server)
    server.AddNext(sink)
    
    RunSimulation()    
    pass