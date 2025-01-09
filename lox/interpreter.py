from typing import Any 

from lox import tokens 
from lox.expr import Visitor, Binary, Grouping, Literal, Unary





class Interpreter(Visitor[Any]):

    def visit_binary_expression(self, expr : Binary) -> str: 
        return tokens.OPERATIONS[expr.operator.type](expr.left.accept(Interpreter), expr.right.accept(Interpreter))

    def visit_grouping_expression(self, expr : Grouping) -> str:
        return expr.expression.accept(Interpreter) 

    def visit_literal_expression(self, expr : Literal) -> str:
        return expr.value 

    def visit_unary_expression(self, expr : Unary) -> str:
        if expr.operator.type == tokens.TokenType.BANG: 
            return not expr.right.accept(Interpreter)
        elif expr.operator.type == tokens.TokenType.MINUS:
            return -expr.right.accept(Interpreter)
        else: 
            return None 