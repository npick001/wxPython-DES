from enum import Enum
from scipy.stats import expon, uniform, triang, norm, weibull_min
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
        self.m_type = Distribution.Type.DEFAULT
        self.m_distribution = None
        pass
    
    def __del__(self):
        pass
    
    def SetParams(self, params):
        # virtual to be overriden
        pass
    
    def GetRV():
        # virtual to be overriden
        pass
    
    pass

class Exponential(Distribution):
    def __init__(self, mean=1):
        super().__init__()
        self.m_type = Distribution.Type.EXPONENTIAL
        self.mean = mean
        self.m_distribution = expon

    def SetParams(self, params):        
        # params is a tuple of the form (mean)
        self.mean = params[0]
        self.m_distribution = expon(scale=self.mean)
        pass

    def GetRV(self):
        return self.m_distribution.rvs()
    
    pass

class Uniform(Distribution):
    def __init__(self, min=0, max=1):
        super().__init__()
        self.m_type = Distribution.Type.UNIFORM
        self.min = min
        self.max = max
        self.m_distribution = uniform

    def SetParams(self, params):
        # params is a tuple of the form (min, max)
        self.min = params[0]
        self.max = params[1]
        self.m_distribution = uniform(loc=self.min, scale=self.max-self.min)
        pass

    def GetRV(self):
        return self.m_distribution.rvs()
    
    pass

class Triangular(Distribution):
    def __init__(self, min=0, mean=1, max=2):
        super().__init__()
        self.m_type = Distribution.Type.TRIANGULAR
        self.min = min
        self.mean = mean
        self.max = max
        c = (mean - min) / (max - min)
        self.m_distribution = triang

    def SetParams(self, params):
        # params is a tuple of the form (min, mean, max)
        self.min = params[0]
        self.mean = params[1]
        self.max = params[2]
        c = (self.mean - self.min) / (self.max - self.min)
        self.m_distribution = triang(c, loc=self.min, scale=self.max-self.min)
        pass

    def GetRV(self):
        return self.m_distribution.rvs()
    
    pass

class Normal(Distribution):
    def __init__(self, mean=1, stdev=0):
        super().__init__()
        self.m_type = Distribution.Type.NORMAL
        self.mean = mean
        self.stdev = stdev
        self.m_distribution = norm

    def SetParams(self, params):
        # params is a tuple of the form (mean, stdev)
        self.mean = params[0]
        self.stdev = params[1]
        self.m_distribution = norm(loc=self.mean, scale=self.stdev)
        pass

    def GetRV(self):
        return self.m_distribution.rvs()
    
    pass

class Weibull(Distribution):
    def __init__(self, shape=0, scale=1):
        super().__init__()
        self.m_type = Distribution.Type.WEIBULL
        self.shape = shape
        self.scale = scale
        self.m_distribution = weibull_min

    def SetParams(self, params):
        # params is a tuple of the form (shape, scale)
        self.shape = params[0]
        self.scale = params[1]
        self.m_distribution = weibull_min(c=self.shape, scale=self.scale)
        pass

    def GetRV(self):
        return self.m_distribution.rvs()
    
    pass



