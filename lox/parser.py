from typing import List 
from lox import state, errors, tokens, lexer, expr

class ParseError(Exception):
    pass 

def parse(lexed_tokens: List[tokens.Token]) -> expr.Expr:
    
    def parse_expression() -> expr.Expr:
        #print("I'm parsing expression!")
        return parse_equality() 

    def parse_equality() -> expr.Expr:
        #print("I'm parsing equality!")
        lhs = parse_comparison() 
        while lexed_tokens and lexed_tokens[0].type in (tokens.TokenType.BANG_EQUAL, tokens.TokenType.EQUAL_EQUAL):
            operator = lexed_tokens.pop(0)
            rhs = parse_comparison()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs

    def parse_comparison() -> expr.Expr:
        #print("I'm parsing comparisons!")
        lhs = parse_term() 
        while lexed_tokens and lexed_tokens[0].type in (tokens.TokenType.GREATER, tokens.TokenType.GREATER_EQUAL, tokens.TokenType.LESSER, tokens.TokenType.LESSER_EQUAL):
            operator = lexed_tokens.pop(0)
            rhs = parse_term()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs
    
    def parse_term() -> expr.Expr:
        #print("I'm parsing terms!")
        lhs = parse_factor() 
        while lexed_tokens and lexed_tokens[0].type in (tokens.TokenType.MINUS, tokens.TokenType.PLUS):
            operator = lexed_tokens.pop(0)
            rhs = parse_factor()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs

    def parse_factor() -> expr.Expr:
        #print("I'm parsing factor!")
        lhs = parse_unary() 
        while lexed_tokens and lexed_tokens[0].type in (tokens.TokenType.TIMES, tokens.TokenType.DIVIDED_BY):
            operator = lexed_tokens.pop(0)
            rhs = parse_unary()
            lhs = expr.Binary(lhs, operator, rhs)
        return lhs
    
    def parse_unary() -> expr.Expr:
        #print("I'm parsing unary!")
        if lexed_tokens and lexed_tokens[0].type in (tokens.TokenType.BANG, tokens.TokenType.MINUS):
            lexed_tokens.pop(0)
            return parse_unary() 
        else: 
            return parse_primary() 

    def parse_primary():
        #print("I'm parsing primary!")
        match lexed_tokens[0].type:
            case tokens.TokenType.NUMBER: 
                return expr.Literal(lexed_tokens.pop(0).value)
            case tokens.TokenType.STRING:
                return expr.Literal(lexed_tokens.pop(0).value)
            case tokens.TokenType.TRUE:
                lexed_tokens.pop(0)
                return expr.Literal(True)
            case tokens.TokenType.FALSE:
                lexed_tokens.pop(0)
                return expr.Literal(False)
            case tokens.TokenType.NIL:
                lexed_tokens.pop(0)
                return expr.Literal(None)
            case tokens.TokenType.IDENTIFIER:
                print("I parsed an identifier!")
                return expr.Literal(lexed_tokens.pop(0).value)
            case tokens.TokenType.LEFT_PAREN:
                lexed_tokens.pop(0)
                temp = parse_expression()
                if lexed_tokens[0].type == tokens.TokenType.RIGHT_PAREN:
                    lexed_tokens.pop(0)
                return temp

    
    return parse_expression()