from lox import state 
from lox import lexer 
from lox import parser
from lox import expr
from lox import errortypes

from lox import uglyprinter
from lox.interpreter import Interpreter

def run(string : str) -> None:

    state.currently_executing_program = string

    if errortypes.mismatch(string):
        print("\n\nLexer uninitialized due to errors caught before Lexing!\n")
        return [] 
    
    alex = lexer.Lexer()
    lexed_tokens = alex.lex(string)
    
    if lexed_tokens:
        new = parser.parse(lexed_tokens)
        #print(lexed_tokens)
        if new: 
            Interpreter.interpret(new)