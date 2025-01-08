from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar  

from lox.tokens import Token 


R = TypeVar('R') #Generic 



class Visitor(Protocol[R]): 
    
    def visit_binary_expression(self, expr : 'Binary') -> R: #forward references
        pass 

    def visit_grouping_expression(self, expr : 'Grouping') -> R:
        pass  

    def visit_literal_expression(self, expr : 'Literal') -> R:
        pass  

    def visit_unary_expression(self, expr : 'Unary') -> R:
        pass  


class Expr(ABC): 
    
    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R:
        pass  

@dataclass
class Binary(Expr):
    left : Expr 
    operator : Token 
    right : Expr  

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary_expression(visitor, self)

@dataclass
class Grouping(Expr):
    expression : Expr 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping_expression(visitor, self)

@dataclass
class Literal(Expr):
    value : Any  

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal_expression(visitor, self)

@dataclass
class Unary(Expr):
    operator : Token 
    right : Expr  

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary_expression(visitor, self)