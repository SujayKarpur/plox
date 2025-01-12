from lox import errors 
from lox import state 

class Environment: 
    

    def __init__(self): 
        self.environment = {}
    
    def __repr__(self):
        return self.environment.__repr__()

    
    def define(self, name, value) -> None:
        self.environment[name] = value 
    
    def get(self, name):
        return self.environment[name]
    
    def set(self, name, value):
        self.environment[name] = value 
        return self.environment[name]