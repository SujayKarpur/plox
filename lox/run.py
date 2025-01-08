from lox import state 
from lox import lexer 


def run(string : str) -> None:
    state.currently_executing_program = string
    lexed_tokens = lexer.lex(string)
    if lexed_tokens:
        print(lexed_tokens)
