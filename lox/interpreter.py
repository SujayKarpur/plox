from typing import Any 
from lox.expr import Visitor, Binary, Grouping, Literal, Unary




class Interpreter(Visitor[Any]):

    def visit_binary_expression(self, expr : Binary) -> str: 
        return None 

    def visit_grouping_expression(self, expr : Grouping) -> str:
        return None 

    def visit_literal_expression(self, expr : Literal) -> str:
        return expr.value 

    def visit_unary_expression(self, expr : Unary) -> str:
        return None 