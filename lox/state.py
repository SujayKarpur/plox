"""
global variables
"""

#GLOBAL CONSTANTS:
KEYWORDS = {'and', 'class', 'else', 'false', 'fun', 'for', 'if', 'nil', 'or', 'print', 'return', 'scan', 'super', 'this', 'true', 'var', 'while'}


error_flag : bool = False 

def reset_error_flag():
    """ set the global error flag to false"""
    global error_flag
    error_flag = False 


current_file_name : str = '<stdin>'
currently_executing_program : str = ''

lexer_row : int = 0 
lexer_column : int = 0 
lexer_position : int = 0 

def reset_lexer(new_lexer_position:int = 0, new_lexer_row:int = 0, new_lexer_column:int = 0) -> None:
    """set all lexer variables to default values"""
    global lexer_row, lexer_column, lexer_position
    lexer_row = new_lexer_row 
    lexer_column = new_lexer_column
    lexer_position = new_lexer_position 


parser_position : int = 0

def reset_parser() -> None:
    pass 

def reset_state() -> None:
    """set all global variables to default values"""
    reset_error_flag()
    reset_lexer()
    reset_parser()

