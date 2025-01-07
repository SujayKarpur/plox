import errors 
import tokens 


def lex(string, verbose=False):
    lexer_position = 0 
    tokens.lexer_row = tokens.lexer_column = 0 
    lexed_tokens = [] 
    max_position = len(string)
    while lexer_position < max_position:
        new_token, forward_position = tokens.TokenType.match(string, lexer_position, tokens.lexer_row, tokens.lexer_column)
        lexer_position += forward_position
        lexed_tokens.append(new_token)
    if not verbose: 
        ignored_tokens = {tokens.TokenType.COMMENT.name, tokens.TokenType.MULTI_LINE_COMMENT.name, tokens.TokenType.SPACE.name, tokens.TokenType.NEWLINE.name, tokens.TokenType.TAB.name}
        lexed_tokens = list(filter(lambda i : i.type not in ignored_tokens, lexed_tokens)) 
    return lexed_tokens