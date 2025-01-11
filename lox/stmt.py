from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypeVar, List

from lox import tokens
from lox import expr 


R = TypeVar('R') #Generic 



class Visitor(Protocol[R]): 

    def visit_block_statement(self, stmt : 'Block') -> R: 
        pass 

    def visit_if_statement(self, stmt : 'If') -> R:
        pass 

    def visit_while_statement(self, stmt : 'While') -> R: 
        pass 

    def visit_print_statement(self, stmt : 'Print') -> R: #forward references
        pass 

    def visit_scan_statement(self, stmt : 'Scan') -> R: 
        pass 

    def visit_expression_statement(self, stmt : 'Expression') -> R:
        pass  

    def visit_variable_statement(self, stmt : 'Var') -> R: 
        pass 

class Stmt(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor[R]): 
        pass 

@dataclass
class Block(Stmt): 
    statements : List[Stmt]

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_block_statement(visitor, self)

@dataclass
class If(Stmt): 
    condition : expr.Expr 
    statement : Stmt 
    else_branch : Stmt 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_if_statement(visitor, self)

@dataclass
class While(Stmt): 
    condition : expr.Expr 
    statement : Stmt 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_while_statement(visitor, self)

@dataclass
class Print(Stmt): 
    expression : expr.Expr

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_print_statement(visitor, self)

@dataclass
class Scan(Stmt): 
    variable : expr.Variable

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_scan_statement(visitor, self)

@dataclass
class Expression(Stmt):
    expression : expr.Expr 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_expression_statement(visitor, self)
    
@dataclass
class Var(Stmt):
    name : tokens.Token 
    initializer : expr.Expr

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_variable_statement(visitor, self)