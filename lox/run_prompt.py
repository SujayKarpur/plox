import curses
import sys 
import termios 
import tty 

from lox import state  
from lox.run import run 



def run_prompt():
    print('Welcome to pLox!\n')
    while True: 
        try:
            print('lox> ', end='')
            line = input()
            run(line+'\n')
            state.reset_REPL()
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt (Press ctrl+D to exit)")
        except EOFError:
            print('\n\nExiting pLox......')
            break 
        except Exception as e: 
            print(f"REPL Exception: {e}")
            break 



if __name__ == '__main__':
    run_prompt()