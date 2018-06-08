import abc
        
class RegressorStrategy(object):
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def fit(self, X, y):
        """Required Method"""
    
    @abc.abstractmethod
    def getSummary(self, model):        
        """Required Method"""        
    
    @abc.abstractmethod
    def getRsquared(self, model):
        """Required Method"""
    
    @abc.abstractmethod
    def getPredictions(self, model, X):
        """Required Method"""
    
    @abc.abstractmethod
    def save_data(self):
        """Required Method"""
        
    @abc.abstractmethod
    def get_saved_data(self):
        """Required Method"""


    
  