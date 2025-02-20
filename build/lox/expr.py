from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar, List 

from lox.tokens import Token 


R = TypeVar('R') #Generic 



class Visitor(Protocol[R]): 
    
    def visit_binary_expression(self, expr : 'Binary') -> R: #forward references
        pass 

    def visit_call_expression(self, expr : 'Call') -> R: 
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

    def visit_index_expression(self, expr : 'Index') -> R:
        pass 
    
    def visit_slice_expression(self, expr : 'Slice') -> R:
        pass 

    def visit_list_expression(self, expr : 'ListExpr') -> R:
        pass 

    def visit_lambda_expression(self, expr : 'Lambda') -> R:
        pass 

    def visit_ternary_expression(self, expr : 'Ternary') -> R:
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
        return visitor.visit_binary_expression(self)

@dataclass
class Call(Expr): 
    callee : Expr 
    arguments : List[Expr]

    def accept(self, visitor : Visitor[R]) -> R: 
        return visitor.visit_call_expression(self)

@dataclass
class Index(Expr):
    list : Expr 
    index : Expr 

    def accept(self, visitor : Visitor[R]) -> R:
        return visitor.visit_index_expression(self)

@dataclass
class Slice(Expr):
    list : Expr 
    start : Expr 
    stop : Expr 
    step : Expr 

    def accept(self, visitor : Visitor[R]) -> R:
        return visitor.visit_slice_expression(self)

@dataclass
class Logical(Expr):
    left : Expr 
    operator : Token 
    right : Expr  

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_logical_expression(self)

@dataclass
class Grouping(Expr):
    expression : Expr 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping_expression(self)

@dataclass
class Literal(Expr):
    value : Any  

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal_expression(self)

@dataclass
class Unary(Expr):
    operator : Token 
    right : Expr  

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary_expression(self)

@dataclass
class Variable(Expr):
    name : Token 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_variable_exression(self)

@dataclass
class Assignment(Expr):
    name : Variable 
    expression : Expr 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_assignment_expression(self)
    

@dataclass
class ListExpr(Expr):
    value : List 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_list_expression(self)
    

@dataclass
class Lambda(Expr):
    parameters : List[Token]
    expression : Expr 

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_lambda_expression(self)


@dataclass
class Ternary(Expr):
    condition : Expr 
    if_condition : Expr 
    else_condition : Expr 

    def accept(self, visitor : Visitor[R]) -> R:
        return visitor.visit_ternary_expression(self)