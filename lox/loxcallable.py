from typing import Protocol
from time import time 

from lox import utils 



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
        print(utils.loxify(arguments[0])) 

    def arity(self) -> int: 
        return 1  

    def __repr__(self) -> str: 
        return "<native fn print>"