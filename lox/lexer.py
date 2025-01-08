from typing import List

from lox import tokens
from lox import state
from lox import errors, errortypes

def lex(string, verbose=False):
    
    if errortypes.mismatch(string):
        print("\n\nLexer uninitialized due to errors caught before Lexing!\n")
        return [] 

    lexed_tokens : List[tokens.Token] = [] 
    MAX_POSITION = len(string)
    while state.lexer_position < MAX_POSITION:
        new_token, forward_position = tokens.TokenType.match(string, state.lexer_position, state.lexer_row, state.lexer_column)
        state.lexer_position += forward_position
        lexed_tokens.append(new_token)
    if not verbose: 
        ignored_tokens = {tokens.TokenType.COMMENT, tokens.TokenType.MULTI_LINE_COMMENT, tokens.TokenType.SPACE, tokens.TokenType.NEWLINE, tokens.TokenType.TAB}
        lexed_tokens = list(filter(lambda i : i.type not in ignored_tokens, lexed_tokens)) 
    return lexed_tokens