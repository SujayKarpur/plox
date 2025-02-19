import curses
import sys 
import termios 
import tty 

from lox import state  
from lox.run import run 
from lox.pipeline import interpreter


def run_prompt():
    print('Welcome to pLox!\n')
    pretty = interpreter.Interpreter()
    while True: 
        try:
            print('lox> ', end='')
            line = input()
            run.run(line+'\n', pretty)
            state.error_flag = False 
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt (Press ctrl+D to exit)")
        except EOFError:
            print('\n\nExiting pLox......')
            break 
        except Exception as e: 
            print(f"REPL Exception: {e}")
            break 


