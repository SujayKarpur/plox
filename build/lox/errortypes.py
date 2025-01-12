#Lexer Errors
#unmatched string/paranthesis/brace/comment
#invalid character
#invalid escape sequence

from lox import state 
from lox import errors

def mismatch(string : str) -> bool:
    
    if string.count("(") != string.count(")"):
        if string.count("(") > string.count(")"):
            errors.report("LexError", state.current_file_name, 0, 0, "unmatched '('")
        else: 
            errors.report("LexError", state.current_file_name, 0, 0, "unmatched ')'")

    if string.count("{") != string.count("}"):
        if string.count("{") > string.count("}"):
            errors.report("LexError", state.current_file_name, 0, 0, "unmatched '{'")
        else: 
            errors.report("LexError", state.current_file_name, 0, 0, "unmatched '}'")

    if string.count("\"") % 2:
        errors.report("LexError", state.current_file_name, 0, 0, "unterminated string literal")

    return state.error_flag