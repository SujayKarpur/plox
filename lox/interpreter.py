from typing import Any 

from lox import tokens 
from lox import errors
from lox import state
from lox import expr 
from lox import stmt 
from lox import utils


    

class Interpreter(expr.Visitor[Any], stmt.Visitor[Any]):

    def visit_binary_expression(self, e : expr.Binary) -> str: 
        left = e.left.accept(Interpreter)
        right = e.right.accept(Interpreter)
        return tokens.OPERATIONS[e.operator.type](left,right)

    def visit_grouping_expression(self, e : expr.Grouping) -> str:
        return e.expression.accept(Interpreter) 

    def visit_literal_expression(self, e : expr.Literal) -> str:
        return e.value 

    def visit_unary_expression(self, e : expr.Unary) -> str:
        if e.operator.type == tokens.TokenType.BANG: 
            eval_temp = e.right.accept(Interpreter)
            return not eval_temp
        elif e.operator.type == tokens.TokenType.MINUS:
            e.right = e.right.accept(Interpreter)
            if type(e.right) == float: 
                return -e.right
            else: 
                errors.report("RuntimeError", state.current_file_name, 1, 1, "Can't negate a non-numeric value!")
        else: 
            return None 

    def visit_print_statement(self, s : stmt.Print):
        print(utils.loxify(s.expression.accept(Interpreter))) 

    def visit_expression_statement(self, s : stmt.Expression):
        return s.expression.accept(Interpreter)  
        