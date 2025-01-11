from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar  

from lox.tokens import Token 


R = TypeVar('R') #Generic 



class Visitor(Protocol[R]): 
    
    def visit_binary_expression(self, expr : 'Binary') -> R: #forward references
        pass 

    def visit_logical_expression(self, expr : 'Logical') -> R: 
        pass 

    def visit_grouping_expression(self, expr : 'Grouping') -> R:
        pass  

    def visit_literal_expression(self, expr : 'Literal') -> R:
        pass  

    def visit_unary_expression(self, expr : 'Unary') -> R:
        pass  

    def visit_variable_exression(self, expr : 'Variable') -> R: 
        pass 

    def visit_assignment_expression(self, expr : 'Assignment') -> R:
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
class Logical(Expr):
    left : Expr 
    operator : Token 
    right : Expr  

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_logical_expression(visitor, self)

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

@dataclass
class Variable(Expr):
    name : Token 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_variable_exression(visitor, self)

@dataclass
class Assignment(Expr):
    name : Variable 
    expression : Expr 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_assignment_expression(visitor, self)