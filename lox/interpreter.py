from typing import Any, List 
import sys 
import copy 

from lox import tokens 
from lox import errors
from lox import state
from lox import expr 
from lox import stmt 
from lox import utils
from lox.loxcallable import LoxCallable


    

class Interpreter(expr.Visitor[Any], stmt.Visitor[Any]):

    def interpret(statements : List[stmt.Stmt]):
        for i in statements:
            i.accept(Interpreter)

    def evaluate(): 
        pass 

    def visit_binary_expression(self, e : expr.Binary) -> str: 
        left = e.left.accept(Interpreter)
        right = e.right.accept(Interpreter)
        return tokens.OPERATIONS[e.operator.type](left,right)

    def visit_logical_expression(self, e : expr.Logical):
        left = e.left.accept(Interpreter)
        if e.operator.type == tokens.TokenType.OR: 
            if left: 
                return left  
        else: 
            if not left:
                return left  
        return e.right.accept(Interpreter)

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
            rhs = e.expression.accept(Interpreter)
            state.Environment[e.name.name.value] = rhs
            self.temp[e.name.name.value] = rhs
            return state.Environment[e.name.name.value]

    def visit_call_expression(self, e : expr.Call):
        callee = e.callee.accept(Interpreter)
        arguments = []
        for i in e.arguments:
            arguments.append(i.accept(Interpreter))

        if not isinstance(callee, LoxCallable):
            errors.report("RuntimeError", state.current_file_name, 1, 1, "Variables must be declared before use!")
            sys.exit()
        new_function : LoxCallable = LoxCallable(callee)
        if len(arguments) != new_function.arity():
            errors.report("RuntimeError", state.current_file_name, 1, 1, "Variables must be declared before use!")
            sys.exit()
        
        return 

    def visit_block_statement(self, s : stmt.Block):
        self.temp = state.Environment.copy()
        Interpreter.interpret(s.statements)
        state.Environment = self.temp  

    def visit_if_statement(self, s : stmt.If):
        if s.condition.accept(Interpreter): 
            s.statement.accept(Interpreter) 
        else:
            if s.else_branch: 
                s.else_branch.accept(Interpreter)

    def visit_while_statement(self, s : stmt.While):
        while s.condition.accept(Interpreter):
            s.statement.accept(Interpreter)

    def visit_for_statement(self, s : stmt.For):
        s.init.accept(Interpreter)
        if iter != None: 
            new_block_statements = stmt.Block([s.statement, stmt.Expression(s.iter)]) 
        else: 
            new_block_statements = s.statement
        if not isinstance(s.condition, stmt.Blank):
            desugar = stmt.While(s.condition, new_block_statements)
        else: 
            desugar = stmt.While(True, new_block_statements)
        desugar.accept(Interpreter)
        
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
    
    def visit_blank_statement(self, stmt):
        pass 