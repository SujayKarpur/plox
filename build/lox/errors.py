from lox import state
from lox import utils 


def report(type: str, file: str , line: int, column: int, message:str) -> None:
    print(f"file {file}, line {line}, column {column}")
    print(f"{utils.nth_line_of_string(state.currently_executing_program, line)}")
    print(" " * column + "^")
    print(f"{type}: {message}")
    #print("[line " + str(line+1) + "] Error" + where + ": " + message)
    state.error_flag = True 

"""def error(type,file,position,row,column,message):
    report(row, "", message)"""