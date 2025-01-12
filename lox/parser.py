from typing import List, Union 
import sys  

from lox import state, tokens, utils 
from lox import expr, stmt


class Parser: 
    """ Implementation of a Recursive Descent Parser for lox. methods corresponding to each rule in the grammar, plus helper methods"""

    def __init__(self, lexed_tokens : List[tokens.Token]) -> None:
        """ initialize parser with a list of lexed tokens """
        self.position : int = 0 
        self.LEXED_TOKENS : List[tokens.Token] = lexed_tokens
        self.MAX_POSITION : int = len(lexed_tokens) - 1


    def end(self) -> bool: 
        """return true iff the parser has parsed all tokens"""
        return self.position > self.MAX_POSITION
    

    def peek(self) -> tokens.Token: 
        """return current token"""
        return self.LEXED_TOKENS[self.position]


    def peek_previous(self) -> tokens.Token:
        """return previously parsed token"""
        return self.LEXED_TOKENS[self.position-1]


    def match(self, expected_token_types: Union[List[tokens.TokenType],tokens.TokenType]) -> bool: 
        """return true if the current token matches expected token(s)"""

        if not utils.supports_in_operator(expected_token_types):
            expected_token_types = [expected_token_types] 

        if not self.end() and self.peek().type in expected_token_types:
            return True 
        else:
            return False     


    def consume(self, expected_token_types: Union[List[tokens.TokenType],tokens.TokenType], error_message:str, optional:bool = False):
        """check for (optionally) expected token(s) at the current position. returns token and moves the parser position forward if it exists"""

        if not utils.supports_in_operator(expected_token_types):
            expected_token_types = [expected_token_types] 

        if not self.end() and self.peek().type in expected_token_types:
            saved = self.peek()
            self.position += 1
            return saved
        else:
            if optional:
                return None 
            #print("The state rn is ", self.position, f"last token processed : {[self.LEXED_TOKENS[self.position-1]]}")
            #errors.report("ParseError", state.current_file_name, 1, 1, error_message)
            #sys.exit()
            self.report(self.peek() if not self.end() else self.peek_previous(), error_message)


    def parse_program(self) -> List[stmt.Stmt]: 
        """program -> (statement)* EOF; outermost parsing rule, a program consists of zero or more statements followed by EOF"""
        statements: List[stmt.Stmt] = []
        while not self.end():
            statements.append(self.parse_declaration())
        return statements
    

    def parse_declaration(self) -> stmt.Stmt:
        """""" #update documentation after adding function declaration

        if self.consume(tokens.TokenType.VAR, "", True):
            name = self.consume(tokens.TokenType.IDENTIFIER, "Expected identifier after `var`!")
            if self.consume(tokens.TokenType.EQUAL, "", True): 
                initializer = self.parse_expression()
                self.consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
                return stmt.Var(name, initializer) 
            else:
                self.consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
                return stmt.Var(name, None)
        else: 
            return self.parse_statement()
        


    def parse_statement(self) -> stmt.Stmt: 
        """statement -> if_statement | while_statement | for_statement | print_statement | scan_statement | block | blank | expression_statement;
        rule for parsing different kinds of statements 
        """

        if self.consume(tokens.TokenType.IF, "", True):                        # if_statement -> if (condition) statement (else statement)? 
            self.consume(tokens.TokenType.LEFT_PAREN, "Expected '(' after `if`!")
            condition = self.parse_expression()
            self.consume(tokens.TokenType.RIGHT_PAREN, "Expected ')' after '('!")
            if_statement = self.parse_statement()
            if self.consume(tokens.TokenType.ELSE, "", True): 
                else_statement = self.parse_statement()
            else:
                else_statement = None 
            return stmt.If(condition, if_statement, else_statement) 
        
        elif self.consume(tokens.TokenType.WHILE, "", True):
            self.consume(tokens.TokenType.LEFT_PAREN, "Expected '(' after `while`!")
            condition = self.parse_expression()
            self.consume(tokens.TokenType.RIGHT_PAREN, "Expected ')'!")
            statement = self.parse_statement()
            return stmt.While(condition, statement) 
        
        elif self.consume(tokens.TokenType.FOR, "", True):
            self.consume(tokens.TokenType.LEFT_PAREN, "Expected '(' after `for`!")
            if self.match(tokens.TokenType.VAR): 
                init = self.parse_declaration() 
            else: 
                init = self.parse_statement()
            condition = self.parse_statement()
            if not self.match(tokens.TokenType.RIGHT_PAREN):
                iter = self.parse_expression()
            else: 
                iter = None 
            self.consume(tokens.TokenType.RIGHT_PAREN, "Expected ')'!")
            statement = self.parse_statement()
            return stmt.For(init, condition, iter, statement) 
        
        elif self.consume(tokens.TokenType.PRINT, "", True):
            new_statement = self.parse_expression()
            self.consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
            return stmt.Print(new_statement) 
        
        elif self.consume(tokens.TokenType.SCAN, "", True):
            name = self.consume(tokens.TokenType.IDENTIFIER, "Expected identifier")
            self.consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
            return stmt.Scan(expr.Variable(name)) 
        
        elif self.consume(tokens.TokenType.LEFT_BRACE, "", True):
            statements: List[stmt.Stmt] = []
            while not self.end() and not self.peek().type == tokens.TokenType.RIGHT_BRACE:
                statements.append(self.parse_declaration())
            self.consume(tokens.TokenType.RIGHT_BRACE, "Expected }!")
            return stmt.Block(statements) 
        
        elif self.consume(tokens.TokenType.SEMICOLON, "", True):
            return stmt.Blank() 
        
        else: 
            new_statement = self.parse_expression()
            self.consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
            return stmt.Expression(new_statement) 



    def parse_expression(self) -> expr.Expr:
        """expression -> assignment; (begin parsing expressions, from lowest to highest priority)"""
        return self.parse_assignment()


    def parse_assignment(self) -> expr.Expr: 
        if (identifier := self.consume(tokens.TokenType.IDENTIFIER, "", True)):
            if self.consume(tokens.TokenType.EQUAL, "", True):
                value = self.parse_expression()
                name = expr.Variable(identifier)
                return expr.Assignment(name, value) 
            else: 
                self.position -= 1
                return self.parse_equality()
        else:
            return self.parse_logic_or() 
        

    def parse_logic_or(self) -> expr.Expr:
        lhs = self.parse_logic_and() 
        while (operator := self.consume(tokens.TokenType.OR, "", True)):
            rhs = self.parse_logic_and()
            lhs = expr.Logical(lhs, operator, rhs)
        return lhs
    

    def parse_logic_and(self) -> expr.Expr: 
        lhs = self.parse_equality() 
        while (operator := self.consume(tokens.TokenType.AND, "", True)):
            rhs = self.parse_equality()
            lhs = expr.Logical(lhs, operator, rhs)
        return lhs


    def parse_equality(self) -> expr.Expr:
        lhs = self.parse_comparison() 
        while (operator := self.consume(tokens.EQUALITY_OPERATORS, "", True)):
            rhs = self.parse_comparison()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs


    def parse_comparison(self) -> expr.Expr:
        lhs = self.parse_term() 
        while (operator := self.consume(tokens.COMPARISON_OPERATORS, "", True)):
            rhs = self.parse_term()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs


    def parse_term(self) -> expr.Expr:
        lhs = self.parse_factor() 
        while (operator := self.consume((tokens.TokenType.MINUS, tokens.TokenType.PLUS), "", True)):
            rhs = self.parse_factor()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs


    def parse_factor(self) -> expr.Expr:
        lhs = self.parse_unary() 
        while (operator := self.consume((tokens.TokenType.TIMES, tokens.TokenType.DIVIDED_BY), "", True)):
            rhs = self.parse_unary()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs


    def parse_unary(self) -> expr.Expr:
        if (operator := self.consume(tokens.UNARY_OPERATORS, "", True)):
            return expr.Unary(operator, self.parse_unary()) 
        else: 
            return self.parse_call() 


    def parse_call(self):
        callee = self.parse_primary()
        while self.consume(tokens.TokenType.LEFT_PAREN, "", True):
            if self.match(tokens.TokenType.RIGHT_PAREN): 
                break  
            else: 
                expression_list : List[expr.Expr] = []  
                expression_list.append(self.parse_expression())
                while self.consume(tokens.TokenType.COMMA, "", True):
                    expression_list.append(self.parse_expression())
        else:
            return callee 
        self.consume(tokens.TokenType.RIGHT_PAREN, "Expected matching ')'!")
        return expr.Call(callee, expression_list)


    def parse_primary(self):

        if (name := self.consume(tokens.TokenType.IDENTIFIER, "", True)):
            return expr.Variable(name)
        elif (literal := self.consume(tokens.LITERAL_OBJECTS, "", True)):
            return expr.Literal(literal.value)
        elif (literal := self.consume(tokens.LITERAL_CONSTANTS, "", True)):
            return expr.Literal(tokens.LITERAL_CONSTANTS[literal])
        elif self.consume(tokens.TokenType.LEFT_PAREN, "", True):
            temp = self.parse_expression()
            self.consume(tokens.TokenType.RIGHT_PAREN, "Expected ')' following '('")
            return temp 
        else: 
            self.report(self.peek(), "expected expression!")


    def parse(self) -> List[stmt.Stmt]:
        """entry point for parsing"""
        try: 
            return self.parse_program()
        except:
            return None 
        

    def report(self, token_with_error : tokens.Token, message : str) -> None:
        
        error_column = token_with_error.column + (len(token_with_error.value) if self.end() else 0)
        print(f"file {state.current_file_name}, line {token_with_error.row+1}, column {error_column}")
        print(f"{utils.nth_line_of_string(state.currently_executing_program, token_with_error.row)}")
        print(" " * (error_column) + "^")
        print(f"ParseError: {message}")
        state.error_flag = True 
        sys.exit()
