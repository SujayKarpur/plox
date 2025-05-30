from typing import Protocol, List
from functools import reduce 
from time import time 

from lox import utils 
from lox import stmt, expr 
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

    def call(self, interpreter, arguments: List): 
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


class Printf(LoxCallable):

    def call(self, interpreter, arguments): 
        arguments = [utils.loxify(x) for x in arguments]
        format_string = arguments.pop(0)
        format_string = format_string.replace("\\n", "\n").replace("\\t", "\t")
        for i in range(len(format_string)):
            if i >0 and format_string[i-1] == '%':
                continue 
            if format_string[i] == '%':
                if format_string[i+1] == '%':
                    print('%', end='')
                elif format_string[i+1] == 'd':
                    print(int(arguments.pop(0)), end='')
                elif format_string[i+1] == 'f':
                    print(float(arguments.pop(0)), end='')
                else:
                    print(arguments.pop(0), end='')
            else:
                print(format_string[i], end='')

    def arity(self) -> int: 
        return 1  

    def __repr__(self) -> str: 
        return "<native fn printf>"


class ListInsert(LoxCallable):

    def call(self, interpreter, arguments): 
        l = arguments[0]
        index = arguments[1]
        value = arguments[2]

    def arity(self) -> int: 
        return 3

    def __repr__(self) -> str: 
        return "<native fn list_insert>"


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


class Len(LoxCallable):

    def call(self, interpreter, arguments):
        return len(arguments[0]) 

    def arity(self) -> int: 
        return 1
    
    def __repr__(self) -> str:
        return "<native fn len>"


class LoxFunction(LoxCallable):

    def __init__(self, declaration : stmt.Function, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments): 
        envy = environment.Environment(interpreter, self.closure)
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



class LoxLambda(LoxCallable):

    def __init__(self, expression : expr.Lambda):
        self.expression = expression 

    def call(self, interpreter, arguments):
        envy = environment.Environment(interpreter, interpreter.globals)
        for i in range(len(self.expression.parameters)):
            envy.define(self.expression.parameters[i].name.value, arguments[i])      

        try:   
            #print(interpreter.evaluate_block(self.expression.expression, envy))
            return interpreter.evaluate_block(self.expression.expression, envy)
        except Return_Exception as retex:
            return retex.value

    def arity(self) -> int:
        return len(self.expression.parameters) 

    def __repr__(self) -> str: 
        return f"<user-defined anonymous function>"