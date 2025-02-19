from typing import Protocol
from functools import reduce 
from time import time 

from lox import utils 
from lox import stmt
from lox import environment

class Return_Exception(Exception):
    def __init__(self, value=None):
        self.value = value


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
        
        if arguments[0] not in {"str", "num"}:
            interpreter.report("First argument to scan must be either 'num' or 'str'!")
        elif arguments[0] == 'str':
            temp = input()
        else:
            temp = float(input())
        return temp

    def arity(self) -> int: 
        return 1

    def __repr__(self) -> str: 
        return "<native fn scan>"
     


class Print(LoxCallable):

    def call(self, interpreter, arguments): 
        for x in arguments:
            print(utils.loxify(x), end=' ')
        print() 

    def arity(self) -> int: 
        return 1  

    def __repr__(self) -> str: 
        return "<native fn print>"


class Map(LoxCallable):

    def call(self, interpreter, arguments):
        pass 

    def arity(self) -> int: 
        return 2 
    
    def __repr__(self) -> str:
        return "<native fn map>"
    

class Filter(LoxCallable):

    def call(self, interpreter, arguments):
        pass 

    def arity(self) -> int: 
        return 2 
    
    def __repr__(self) -> str:
        return "<native fn filter>"


class Reduce(LoxCallable):

    def call(self, interpreter, arguments):
        pass 

    def arity(self) -> int: 
        return 2 
    
    def __repr__(self) -> str:
        return "<native fn reduce>"


class LoxFunction(LoxCallable):

    def __init__(self, declaration : stmt.Function):
        self.declaration = declaration

    def call(self, interpreter, arguments): 
        envy = environment.Environment(interpreter, interpreter.globals)
        for i in range(len(self.declaration.params)):
            envy.define(self.declaration.params[i].name.value, arguments[i]) 
        try:
            interpreter.execute_block(self.declaration.body, envy)
        except Return_Exception as retex:
            return retex.value

    def arity(self) -> int: 
        return len(self.declaration.params)  

    def __repr__(self) -> str: 
        return f"<user-defined fn {self.declaration.name}>"