import random
from enum import Enum

## SHOULD BE COMPLETED FOR NOW
## DISTRIBUTIONS WERE TRIMMED TO ONES I'D 
## ACTUALLY USE

class Distribution:
    class Type(Enum):
        DEFAULT = "Base Distribution"
        EXPONENTIAL = "Exponential"
        UNIFORM = "Uniform"
        TRIANGULAR = "Triangular"
        NORMAL = "Normal"
        WEIBULL = "Weibull"
    
    def __init__(self) -> None:
        # type to be overriden by children
        self.m_type = self.Type.DEFAULT
        pass
    
    def __del__(self):
        pass
    
    def GetRV():
        # virtual to be overriden
        pass
    
    def Uniform_0_1():       
        random.seed() 
        return random.uniform(0, 1)
    
    pass

class Exponential(Distribution):
    def __init__(self, mean):
        
        self.m_type = self.Type.EXPONENTIAL
        self.mean = mean        
        pass
    
    def __del__(self):
        pass
    
    def GetRV(self):
        random.seed() 
        return random.expovariate(self.mean)
    
    pass

class Uniform(Distribution):
    def __init__(self, min, max):

        self.m_type = self.Type.UNIFORM
        self.min = min
        self.max = max        
        pass
    
    def __del__(self):
        pass
    
    def GetRV(self):
        
        random.seed() 
        return random.uniform(self.min, self.max)
    
    pass

class Triangular(Distribution):
    def __init__(self, min, mean, max):
        
        self.m_type = self.Type.TRIANGULAR
        self.min = min
        self.mean = mean
        self.max = max
        pass
    
    def __del__(self):
        pass
    
    def GetRV(self):
        
        random.seed() 
        return random.triangular(self.min, self.mean, self.max)
    
    pass

class Normal(Distribution):
    def __init__(self, mean, stdev) -> None:

        self.m_type = self.Type.NORMAL
        self.mean = mean
        self.stdev = stdev
        pass
    
    def __del__(self):
        pass
    
    def GetRV(self):
        
        random.seed() 
        return random.normalvariate(self.mean, self.stdev)
    
    pass

class Weibull(Distribution):
    def __init__(self, shape, scale) -> None:

        self.m_type = self.Type.WEIBULL
        self.shape = shape
        self.scale = scale
        pass
    
    def __del__(self):
        pass
    
    def GetRV(self):
        
        random.seed() 
        return random.weibullvariate(self.shape, self.scale)
    
    pass



