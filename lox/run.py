from lox import state 
from lox import lexer 
from lox import parser
from lox import expr

from lox import uglyprinter
from lox.interpreter import Interpreter, Statement_Interpreter

def run(string : str) -> None:
    state.currently_executing_program = string
    lexed_tokens = lexer.lex(string)
    if lexed_tokens:
        new = parser.parse(lexed_tokens)
        print(lexed_tokens)
        if new: 
            print('\n'*3)
            for i in new:
                print(i.accept(Statement_Interpreter)) 