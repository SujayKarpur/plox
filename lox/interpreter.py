from typing import Any, List, Union 
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

    def interpret(self, statements : Union[List[stmt.Stmt],stmt.Stmt]):
        try:
            for i in statements:
                i.accept(self)
        except: 
            statements.accept(self)

    def evaluate(self, expression : expr.Expr): 
        return expression.accept(self) 

    def visit_binary_expression(self, e : expr.Binary) -> str: 
        left = self.evaluate(e.left)
        right = self.evaluate(e.right)
        return tokens.OPERATIONS[e.operator.type](left,right)

    def visit_logical_expression(self, e : expr.Logical):
        left = self.evaluate(e.left)
        if e.operator.type == tokens.TokenType.OR: 
            if left: 
                return left  
        else: 
            if not left:
                return left  
        return self.evaluate(e.right)

    def visit_grouping_expression(self, e : expr.Grouping) -> str:
        return self.evaluate(e.expression)

    def visit_literal_expression(self, e : expr.Literal) -> str:
        return e.value 

    def visit_unary_expression(self, e : expr.Unary) -> str:
        if e.operator.type == tokens.TokenType.BANG: 
            eval_temp = self.evaluate(e.right)
            return not eval_temp
        elif e.operator.type == tokens.TokenType.MINUS:
            e.right = self.evaluate(e.right)
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
            rhs = self.evaluate(e.expression)
            state.Environment[e.name.name.value] = rhs
            self.temp[e.name.name.value] = rhs
            return state.Environment[e.name.name.value]

    def visit_call_expression(self, e : expr.Call):
        callee = self.evaluate(e.callee)
        arguments = []
        for i in e.arguments:
            arguments.append(self.evaluate(i))

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
        self.interpret(s.statements)
        state.Environment = self.temp  

    def visit_if_statement(self, s : stmt.If):
        if self.evaluate(s.condition): 
            self.interpret(s.statement)
        else:
            if s.else_branch: 
                self.interpret(s.else_branch)

    def visit_while_statement(self, s : stmt.While):
        while self.evaluate(s.condition):
            self.interpret(s.statement)

    def visit_for_statement(self, s : stmt.For):
        if isinstance(s.init, expr.Expr):
            s.init = stmt.Expression(s.init)
        self.interpret(s.init)
        if iter != None: 
            new_block_statements = stmt.Block([s.statement, stmt.Expression(s.iter)]) 
        else: 
            new_block_statements = s.statement
        if not isinstance(s.condition, stmt.Blank):
            desugar = stmt.While(s.condition, new_block_statements)
        else: 
            desugar = stmt.While(True, new_block_statements)
        self.interpret(desugar)
        
    def visit_print_statement(self, s : stmt.Print):
        print(utils.loxify(self.evaluate(s.expression))) 

    def visit_scan_statement(self, s : stmt.Scan):
        temp = input() #fix later; shouldn't be input, should lex/parse the string
        state.Environment[s.variable.name.value] = temp

    def visit_expression_statement(self, s : stmt.Expression):
        return self.evaluate(s.expression) 
    
    def visit_variable_statement(self, s : stmt.Var):
        try:
            state.Environment[s.name.value] = self.evaluate(s.initializer)
        except:
            state.Environment[s.name.value] = None 
    
    def visit_blank_statement(self, s):
        pass 