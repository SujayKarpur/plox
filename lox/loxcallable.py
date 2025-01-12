from typing import Protocol
from time import time 

class LoxCallable(Protocol): 

    def call(self, interpreter, arguments): 
        pass 

    def arity(self) -> int:
        pass 



class Clock(LoxCallable):

    def call(self, interpreter, arguments): 
        return float(time()) 

    def arity(self) -> int: 
        return 0  
    
    def __repr__(self) -> str:
        return "<native fn clock>"


class Scan(LoxCallable):

    def call(self, interpreter, arguments): 
        pass 

    def arity(self) -> int: 
        return 2 

    def __repr__(self) -> str: 
        return "<native fn scan>"
     


class Print(LoxCallable):

    def call(self, interpreter, arguments): 
        pass 

    def arity(self) -> int: 
        pass 

    def __repr__(self) -> str: 
        return "<native fn print>"