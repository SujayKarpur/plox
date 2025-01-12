"""
global variables
"""

#GLOBAL CONSTANTS:
KEYWORDS = {'and', 'class', 'else', 'false', 'fun', 'for', 'if', 'nil', 'or', 'print', 'return', 'super', 'this', 'true', 'var', 'while'} #'scan'


error_flag : bool = False 

def reset_error_flag():
    """ set the global error flag to false"""
    global error_flag
    error_flag = False 


current_file_name : str = '<stdin>'
currently_executing_program : str = ''


pretty = None 



def reset_REPL() -> None: 
    reset_error_flag()





def reset_state() -> None:
    """set all global variables to default values"""
    reset_REPL()
