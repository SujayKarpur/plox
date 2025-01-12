

class Environment: 
    

    def __init__(self, parent, enclosing = None): 
        self.environment = {}
        self.parent = parent 
        self.enclosing = enclosing 
    
    def __repr__(self):
        return self.environment.__repr__() + " " + str(self.enclosing)

    
    def define(self, name, value) -> None:
        self.environment[name] = value 
    
    def get(self, name):
        try:
            return self.environment[name]
        except: 
            try: 
                if self.enclosing: 
                    return self.enclosing.get(name)
                else:
                    raise EOFError
                    #self.parent.report("Variables must be declared before use!")
            except:
                self.parent.report("Variables must be declared before use!")
    
    def set(self, name, value):
        try:
            x = self.environment[name]
            self.environment[name] = value 
            return self.environment[name] 
        except: 
            try:
                if self.enclosing: 
                    return self.enclosing.set(name, value)
            except: 
                self.parent.report("Variables must be declared before use!")
    
    def copy(self):
        new = Environment(self.parent, self.enclosing)
        new.environment = self.environment
        return new