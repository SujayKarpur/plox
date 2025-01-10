from typing import List 
import sys  

from lox import state, errors, tokens
from lox import expr, stmt

class ParseError(Exception):
    pass 


def parser_end() -> bool:
    return state.parser_position > state.max_parser_position


def parse_program(lexed_tokens: List[tokens.Token]) -> List[stmt.Stmt]: 
    statements: List[stmt.Stmt] = []
    while state.parser_position <= state.max_parser_position:
        statements.append(parse_statement(lexed_tokens))
        state.reset_parser(state.parser_position+1)
    return statements

def parse_statement(lexed_tokens: List[tokens.Token]) -> stmt.Stmt: 
    if lexed_tokens[state.parser_position].type == tokens.TokenType.PRINT:
        print("i'm parsing print!!")
        state.reset_parser(state.parser_position+1)
        new_statement = parse_expression(lexed_tokens)
        print(lexed_tokens, state.parser_position)
        if parser_end() or lexed_tokens[state.parser_position].type != tokens.TokenType.SEMICOLON:
            errors.report("ParseError", state.current_file_name, 1, 1, "Missing semicolon!")
            sys.exit()
        else: 
            state.reset_parser(state.parser_position+1)
            return stmt.Print(new_statement) 
    else: 
        new_statement = parse_expression(lexed_tokens)
        if parser_end() or lexed_tokens[state.parser_position].type != tokens.TokenType.SEMICOLON:
            errors.report("ParseError", state.current_file_name, 1, 1, "Missing semicolon!")
            sys.exit()
        else: 
            state.reset_parser(state.parser_position+1)
            return stmt.Expression(new_statement) 
        
def parse_expression(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    return parse_equality(lexed_tokens) 

def parse_equality(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    lhs = parse_comparison(lexed_tokens) 
    while not parser_end() and lexed_tokens[state.parser_position].type in tokens.EQUALITY_OPERATORS:
        operator = lexed_tokens[state.parser_position]
        state.reset_parser(state.parser_position+1)
        rhs = parse_comparison(lexed_tokens)
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_comparison(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    lhs = parse_term(lexed_tokens) 
    while not parser_end() and lexed_tokens[state.parser_position].type in tokens.COMPARISON_OPERATORS:
        operator = lexed_tokens[state.parser_position]
        state.reset_parser(state.parser_position+1)
        rhs = parse_term(lexed_tokens)
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_term(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    lhs = parse_factor(lexed_tokens) 
    while not parser_end() and lexed_tokens[state.parser_position].type in (tokens.TokenType.MINUS, tokens.TokenType.PLUS):
        operator = lexed_tokens[state.parser_position]
        state.reset_parser(state.parser_position+1)
        rhs = parse_factor(lexed_tokens)
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_factor(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    lhs = parse_unary(lexed_tokens) 
    while not parser_end() and lexed_tokens[state.parser_position].type in (tokens.TokenType.TIMES, tokens.TokenType.DIVIDED_BY):
        operator = lexed_tokens[state.parser_position]
        state.reset_parser(state.parser_position+1)
        rhs = parse_unary(lexed_tokens)
        lhs = expr.Binary(lhs, operator, rhs)
    return lhs

def parse_unary(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    if not parser_end() and lexed_tokens[state.parser_position].type in tokens.UNARY_OPERATORS:
        operator = lexed_tokens[state.parser_position]
        state.reset_parser(state.parser_position+1)
        return expr.Unary(operator, parse_unary()) 
    else: 
        return parse_primary(lexed_tokens) 

def parse_primary(lexed_tokens: List[tokens.Token]):
    match lexed_tokens[state.parser_position].type:
        case temp_tok if temp_tok in tokens.LITERAL_OBJECTS: 
            literal = lexed_tokens[state.parser_position]
            state.reset_parser(state.parser_position+1)
            return expr.Literal(literal.value)
        case temp_tok if temp_tok in tokens.LITERAL_CONSTANTS:
            state.reset_parser(state.parser_position+1)
            return expr.Literal(tokens.LITERAL_CONSTANTS[temp_tok])
        case tokens.TokenType.LEFT_PAREN:
            state.reset_parser(state.parser_position+1)
            temp = parse_expression(lexed_tokens)
            if not parser_end() and lexed_tokens[state.parser_position].type == tokens.TokenType.RIGHT_PAREN:
                state.reset_parser(state.parser_position+1)
            return temp
        case _: 
            errors.report("ParseError", state.current_file_name, 1, 1, "Expected an expression!") 
    

def parse(lexed_tokens : List[tokens.Token]) -> List[stmt.Stmt]:
    try: 
        return parse_program(lexed_tokens)
    except:
        return None 