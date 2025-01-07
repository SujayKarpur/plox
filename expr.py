from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar  

from tokens import Token 





class Expr(ABC): 
    
    @abstractmethod
    def accept():
        pass  

@dataclass
class Binary(Expr):
    left : Expr 
    operator : Token 
    right : Expr  

@dataclass
class Grouping(Expr):
    expression : Expr 

@dataclass
class Literal(Expr):
    value : Any  

@dataclass
class Unary(Expr):
    operator : Token 
    right : Expr  