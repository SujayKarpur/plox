from typing import Any 

from lox import tokens 
from lox import errors
from lox import state
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
            expr.right = expr.right.accept(Interpreter)
            if type(expr.right) == float: 
                return -expr.right
            else: 
                errors.report("RuntimeError", state.current_file_name, 1, 1, "Can't negate a non-numeric value!")
        else: 
            return None 