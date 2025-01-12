from typing import Any, List, Union 
import sys 

from lox import tokens 
from lox import state
from lox import expr 
from lox import stmt 
from lox import utils
from lox import environment
from lox.loxcallable import LoxCallable, Clock, Scan, Print, LoxFunction, Return_Exception







class Interpreter(expr.Visitor[Any], stmt.Visitor[Any]):
#later : make scan and print builtin functions instead of keywords

    def __init__(self):
        self.globals = environment.Environment(self)
        self.environment = self.globals
        self.last_line = 1
        self.last_executed_statement = None 
        self.globals.define('clock', Clock())
        self.globals.define('scan', Scan())
        self.globals.define('print', Print())

    def interpret(self, statements : Union[List[stmt.Stmt],stmt.Stmt]) -> None:
        if type(statements) == list:
            for i in statements:
                self.last_executed_statement = i
                i.accept(self)
                self.last_line += 1
        else: 
            self.last_executed_statement = statements
            statements.accept(self)

    def execute(self, statement : stmt.Stmt) -> None:
        statement.accept(self) 


    def execute_block(self, statements : List[stmt.Stmt], envy : environment.Environment) -> None:
        previous : environment.Environment = self.environment#.copy()
        try:
            self.environment = envy#.copy()
            for i in statements: 
                self.interpret(i) 
        finally:
            self.environment = previous#.copy()


    def evaluate(self, expression : expr.Expr): 
        #print('eva', expression.accept(self) )
        return expression.accept(self) 
    
    
    def report(self, message : str) -> None:
        print(f"\nfile {state.current_file_name}, line {self.last_line}")
        print(f"{self.last_executed_statement}")
        print(f"RuntimeError: {message}") 
        state.error_flag = True 
        sys.exit()


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
            rhs = self.evaluate(e.right)
            if type(rhs) == float: 
                return -rhs
            else: 
                self.report("Can't negate a non-numeric value!")
        else: 
            return None 
    

    def visit_variable_exression(self, e : expr.Variable):
        return self.environment.get(e.name.value)
    

    def visit_assignment_expression(self, e : expr.Assignment):
        rhs = self.evaluate(e.expression)
        return self.environment.set(e.name.name.value, rhs)


    def visit_call_expression(self, e : expr.Call):

        callee = self.evaluate(e.callee)
        arguments = []

        for i in e.arguments:
            arguments.append(self.evaluate(i))

        if not hasattr(callee, "call"):
            self.report("can't call a non-callable object")

        if len(arguments) != callee.arity():
            self.report(f"The function expected {callee.arity()} arguments but received {len(arguments)} arguments")

        return callee.call(self, arguments)


    def visit_block_statement(self, s : stmt.Block):
        self.execute_block(s.statements, environment.Environment(self, self.environment))


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
        self.environment.set(s.variable.name.value, temp)


    def visit_expression_statement(self, s : stmt.Expression):
        self.evaluate(s.expression) 
    

    def visit_variable_statement(self, s : stmt.Var):
        try:
            initial_value = self.evaluate(s.initializer)
        except:
            initial_value = None
        finally:
            self.environment.define(s.name.value, initial_value)
    

    def visit_blank_statement(self, s):
        pass 


    def visit_function_statement(self, s : stmt.Function):
        
        func : LoxFunction = LoxFunction(s)
        self.environment.define(s.name.value, func)
    
    def visit_return_statement(self, s : stmt.Return):
        value = None 
        if s.value: 
            value = self.evaluate(s.value)
        raise Return_Exception(value)