from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypeVar

from lox import expr 


R = TypeVar('R') #Generic 



class Visitor(Protocol[R]): 
    
    def visit_print_statement(self, stmt : 'Print') -> R: #forward references
        pass 

    def visit_expression_statement(self, stmt : 'Expression') -> R:
        pass  


class Stmt(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor[R]): 
        pass 


@dataclass
class Print(Stmt): 
    expression : expr.Expr

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_print_statement(visitor, self)

@dataclass
class Expression(Stmt):
    expression : expr.Expr 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_expression_statement(visitor, self)