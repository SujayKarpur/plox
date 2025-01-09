from lox import state 
from lox import lexer 
from lox import parser
from lox import expr

from lox import uglyprinter
from lox.interpreter import Interpreter

def run(string : str) -> None:
    state.currently_executing_program = string
    lexed_tokens = lexer.lex(string)
    if lexed_tokens:
        print(lexed_tokens,'\n'*3)
        new_expr = parser.parse(lexed_tokens)
        print(new_expr.accept(uglyprinter.Printer))
        print("\n"*3)
        print(new_expr.accept(Interpreter))