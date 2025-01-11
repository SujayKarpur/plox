from typing import List 
import sys  

from lox import state, errors, tokens
from lox import expr, stmt


LEXED_TOKENS : List[tokens.Token] 

def supports_in_operator(obj):
    return hasattr(obj, "__contains__")


def parser_end() -> bool:
    return state.parser_position > state.max_parser_position


def consume(expected_token_types, error_message:str, optional:bool = False):
    if not supports_in_operator(expected_token_types):
        expected_token_types = [expected_token_types] 
    if not parser_end() and LEXED_TOKENS[state.parser_position].type in expected_token_types:
        state.reset_parser(state.parser_position+1)
        return LEXED_TOKENS[state.parser_position-1] 
    else:
        if optional:
            return None 
        print("The state rn is ", state.parser_position, f"last token processed : {[LEXED_TOKENS[state.parser_position-1]]}")
        errors.report("ParseError", state.current_file_name, 1, 1, error_message)
        sys.exit()


def parse_program() -> List[stmt.Stmt]: 
    #print("I'm parsing program!")
    statements: List[stmt.Stmt] = []
    while not parser_end():
        statements.append(parse_declaration())
        #state.reset_parser(state.parser_position+1)
    return statements

def parse_declaration() -> stmt.Stmt:
    if consume(tokens.TokenType.VAR, "", True):
        name = consume(tokens.TokenType.IDENTIFIER, "Expected identifier")
        if consume(tokens.TokenType.EQUAL, "", True): 
            initializer = parse_expression()
            consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
            return stmt.Var(name, initializer) 
        else:
            consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
            return stmt.Var(name, None)
    else: 
        return parse_statement()

def parse_statement() -> stmt.Stmt: 
    if consume(tokens.TokenType.PRINT, "", True):
        new_statement = parse_expression()
        consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
        return stmt.Print(new_statement) 
    elif consume(tokens.TokenType.SCAN, "", True):
        name = consume(tokens.TokenType.IDENTIFIER, "Expected identifier")
        consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
        return stmt.Scan(expr.Variable(name)) 
    elif consume(tokens.TokenType.LEFT_BRACE, "", True):
        statements: List[stmt.Stmt] = []
        while not parser_end() and not LEXED_TOKENS[state.parser_position].type == tokens.TokenType.RIGHT_BRACE:
            statements.append(parse_declaration())
        consume(tokens.TokenType.RIGHT_BRACE, "Expected }!")
        return stmt.Block(statements) 
    else: 
        new_statement = parse_expression()
        consume(tokens.TokenType.SEMICOLON, "Missing semicolon")
        return stmt.Expression(new_statement) 
        
def parse_expression() -> expr.Expr:
    return parse_assignment()

def parse_assignment() -> expr.Expr: 
    if (identifier := consume(tokens.TokenType.IDENTIFIER, "", True)):
        if consume(tokens.TokenType.EQUAL, "", True):
            value = parse_expression()
            name = expr.Variable(identifier)
            return expr.Assignment(name, value) 
        else: 
            state.reset_parser(state.parser_position-1) 
            return parse_equality()
    else:
        return parse_equality() 

def parse_equality() -> expr.Expr:
    lhs = parse_comparison() 
    while (operator := consume(tokens.EQUALITY_OPERATORS, "", True)):
        rhs = parse_comparison()
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_comparison() -> expr.Expr:
    lhs = parse_term() 
    while (operator := consume(tokens.COMPARISON_OPERATORS, "", True)):
        rhs = parse_term()
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_term() -> expr.Expr:
    lhs = parse_factor() 
    while (operator := consume((tokens.TokenType.MINUS, tokens.TokenType.PLUS), "", True)):
        rhs = parse_factor()
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_factor() -> expr.Expr:
    lhs = parse_unary() 
    while (operator := consume((tokens.TokenType.TIMES, tokens.TokenType.DIVIDED_BY), "", True)):
        rhs = parse_unary()
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_unary() -> expr.Expr:
    if (operator := consume(tokens.UNARY_OPERATORS, "", True)):
        return expr.Unary(operator, parse_unary()) 
    else: 
        return parse_primary() 

def parse_primary():
    match LEXED_TOKENS[state.parser_position].type:
        case tokens.TokenType.IDENTIFIER: 
            name = LEXED_TOKENS[state.parser_position]
            state.reset_parser(state.parser_position+1)
            return expr.Variable(name)
        case temp_tok if temp_tok in tokens.LITERAL_OBJECTS: 
            literal = LEXED_TOKENS[state.parser_position]
            state.reset_parser(state.parser_position+1)
            return expr.Literal(literal.value)
        case temp_tok if temp_tok in tokens.LITERAL_CONSTANTS:
            state.reset_parser(state.parser_position+1)
            return expr.Literal(tokens.LITERAL_CONSTANTS[temp_tok])
        case tokens.TokenType.LEFT_PAREN:
            state.reset_parser(state.parser_position+1)
            temp = parse_expression()
            if not parser_end() and LEXED_TOKENS[state.parser_position].type == tokens.TokenType.RIGHT_PAREN:
                state.reset_parser(state.parser_position+1)
            return temp
        case _: 
            errors.report("ParseError", state.current_file_name, 1, 1, "Expected an expression!") 
    

def parse(lexed_tokens : List[tokens.Token]) -> List[stmt.Stmt]:
    try: 
        global LEXED_TOKENS
        LEXED_TOKENS = lexed_tokens
        return parse_program()
    except:
        return None 