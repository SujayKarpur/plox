from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypeVar, List, Union 

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

    def visit_for_statement(self, stmt : 'For') -> R: 
        pass 

    def visit_print_statement(self, stmt : 'Print') -> R: #forward references
        pass 

    def visit_scan_statement(self, stmt : 'Scan') -> R: 
        pass 

    def visit_expression_statement(self, stmt : 'Expression') -> R:
        pass  

    def visit_variable_statement(self, stmt : 'Var') -> R: 
        pass 

    def visit_blank_statement(self, stmt : 'Blank') -> R:
        pass 

    def visit_function_statement(self, stmt : 'Function') -> R: 
        pass 
    

class Stmt(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor[R]): 
        pass 

@dataclass
class Block(Stmt): 
    statements : List[Stmt]

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_block_statement(self)

@dataclass
class If(Stmt): 
    condition : expr.Expr 
    statement : Stmt 
    else_branch : Stmt 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_if_statement(self)

@dataclass
class While(Stmt): 
    condition : expr.Expr 
    statement : Stmt 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_while_statement(self)

@dataclass
class For(Stmt): 
    init : Union[expr.Expr, 'Var', 'Blank']
    condition : expr.Expr 
    iter : expr.Expr 
    statement : Stmt 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_for_statement(self)

@dataclass
class Print(Stmt): 
    expression : expr.Expr

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_print_statement(self)

@dataclass
class Scan(Stmt): 
    variable : expr.Variable

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_scan_statement(self)

@dataclass
class Expression(Stmt):
    expression : expr.Expr 

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_expression_statement(self)
    
@dataclass
class Var(Stmt):
    name : tokens.Token 
    initializer : expr.Expr

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_variable_statement(self)

@dataclass
class Blank(Stmt):

    def accept(self, visitor: Visitor[R]):
        return visitor.visit_blank_statement(self)
    

@dataclass
class Function(Stmt):
    name : tokens.Token
    params : List[tokens.Token]
    body : List[Stmt]

    def accept(self, visitor : Visitor[R]):
        return visitor.visit_function_statement(self)