from typing import Any 
import sys 

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
    
    def visit_variable_exression(self, e : expr.Variable):
        if e.name.value not in state.Environment:
            errors.report("RuntimeError", state.current_file_name, 1, 1, "Variables must be declared before use!")
            sys.exit()
        return state.Environment[e.name.value]

    def visit_assignment_expression(self, e : expr.Assignment):
        if e.name.name.value not in state.Environment: 
            errors.report("RuntimeError", state.current_file_name, 1, 1, "Variables must be declared before use!")
            sys.exit()
        else: 
            state.Environment[e.name.name.value] = e.expression.accept(Interpreter)
            return state.Environment[e.name.name.value]

    def visit_print_statement(self, s : stmt.Print):
        print(utils.loxify(s.expression.accept(Interpreter))) 

    def visit_scan_statement(self, s : stmt.Scan):
        temp = input() #fix later; shouldn't be input, should lex/parse the string
        state.Environment[s.variable.name.value] = temp
        #print(utils.loxify(s.expression.accept(Interpreter))) 

    def visit_expression_statement(self, s : stmt.Expression):
        return s.expression.accept(Interpreter)  
    
    def visit_variable_statement(self, s : stmt.Var):
        try:
            state.Environment[s.name.value] = s.initializer.accept(Interpreter) 
        except:
            state.Environment[s.name.value] = None 