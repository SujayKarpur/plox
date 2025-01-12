from lox import state 
from lox import lexer 
from lox import parser
from lox import errortypes

from lox.interpreter import Interpreter

def run(string : str) -> None:

    state.currently_executing_program = string

    if errortypes.mismatch(string):
        print("\n\nLexer uninitialized due to errors caught before Lexing!\n")
        return [] 
    
    alex = lexer.Lexer(string)
    lexed_tokens = alex.lex()

    if lexed_tokens:
        happy = parser.Parser(lexed_tokens)
        new = happy.parse()
        if new: 
            pretty = Interpreter()
            pretty.interpret(new)