import curses

from lox import state  
from lox.run import run 



def run_prompt():
    print('Welcome to pLox!\n')
    try:
        while True: 
            print('lox> ', end='')
            line = input()
            run(line+'\n')
            state.reset_state()
    except EOFError:
        print('\n\nExiting pLox......')



if __name__ == '__main__':
    run_prompt()