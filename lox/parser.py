from typing import List 
from lox import state, errors, tokens, lexer, expr

class ParseError(Exception):
    pass 

def parse(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    
    def parse_expression() -> expr.Expr:
        return parse_equality() 

    def parse_equality() -> expr.Expr:
        lhs = parse_comparison() 
        while lexed_tokens and lexed_tokens[0].type in tokens.EQUALITY_OPERATORS:
            operator = lexed_tokens.pop(0)
            rhs = parse_comparison()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs

    def parse_comparison() -> expr.Expr:
        lhs = parse_term() 
        while lexed_tokens and lexed_tokens[0].type in tokens.COMPARISON_OPERATORS:
            operator = lexed_tokens.pop(0)
            rhs = parse_term()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs
    
    def parse_term() -> expr.Expr:
        lhs = parse_factor() 
        while lexed_tokens and lexed_tokens[0].type in (tokens.TokenType.MINUS, tokens.TokenType.PLUS):
            operator = lexed_tokens.pop(0)
            rhs = parse_factor()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs

    def parse_factor() -> expr.Expr:
        lhs = parse_unary() 
        while lexed_tokens and lexed_tokens[0].type in (tokens.TokenType.TIMES, tokens.TokenType.DIVIDED_BY):
            operator = lexed_tokens.pop(0)
            rhs = parse_unary()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs
    
    def parse_unary() -> expr.Expr:
        if lexed_tokens and lexed_tokens[0].type in tokens.UNARY_OPERATORS:
            return expr.Unary(lexed_tokens.pop(0), parse_unary()) 
        else: 
            return parse_primary() 

    def parse_primary():
        match lexed_tokens[0].type:
            case temp_tok if temp_tok in tokens.LITERAL_OBJECTS: 
                return expr.Literal(lexed_tokens.pop(0).value)
            case temp_tok if temp_tok in tokens.LITERAL_CONSTANTS:
                lexed_tokens.pop(0)
                return expr.Literal(tokens.LITERAL_CONSTANTS[temp_tok])
            case tokens.TokenType.LEFT_PAREN:
                lexed_tokens.pop(0)
                temp = parse_expression()
                if lexed_tokens[0].type == tokens.TokenType.RIGHT_PAREN:
                    lexed_tokens.pop(0)
                return temp
            case _: 
                errors.report("ParseError", state.current_file_name, 1, 1, "Expected an expression!") 
    
    return parse_expression()