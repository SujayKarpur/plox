from typing import Any 

from lox import tokens 
from lox import errors
from lox import state
from lox.expr import Visitor, Binary, Grouping, Literal, Unary
from lox import stmt 

def loxify(f):

    if f is True:
        return "true"
    elif f is False: 
        return "false" 
    elif f == None:
        return "nil"
    else:
        return f 
    

class Interpreter(Visitor[Any]):

    def visit_binary_expression(self, expr : Binary) -> str: 
        left = expr.left.accept(Interpreter)
        right = expr.right.accept(Interpreter)
        return tokens.OPERATIONS[expr.operator.type](left,right)

    def visit_grouping_expression(self, expr : Grouping) -> str:
        return expr.expression.accept(Interpreter) 

    def visit_literal_expression(self, expr : Literal) -> str:
        return expr.value 

    def visit_unary_expression(self, expr : Unary) -> str:
        if expr.operator.type == tokens.TokenType.BANG: 
            eval_temp = expr.right.accept(Interpreter)
            return not eval_temp
        elif expr.operator.type == tokens.TokenType.MINUS:
            expr.right = expr.right.accept(Interpreter)
            if type(expr.right) == float: 
                return -expr.right
            else: 
                errors.report("RuntimeError", state.current_file_name, 1, 1, "Can't negate a non-numeric value!")
        else: 
            return None 
        
class Statement_Interpreter(stmt.Visitor[Any]):
    
    def visit_print_statement(self, s : stmt.Print):
        print(loxify(s.expression.accept(Interpreter))) 

    def visit_expression_statement(self, s : stmt.Expression):
        return s.expression.accept(Interpreter)  