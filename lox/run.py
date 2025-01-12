from lox import state 
from lox import lexer 
from lox import parser
from lox import errortypes

from lox import interpreter

def run(string : str, interpreter_lox : interpreter.Interpreter) -> None:

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
            try:
                interpreter_lox.interpret(new)
            except:
                pass 
        else:
            print("no parse")