import sys 

from lox.run import run
from lox import state 


def run_script(file):
    f = open(file, 'r')
    contents = f.read()
    state.reset_state()
    state.current_file_name = file 
    run(contents)
    if state.error_flag:
        sys.exit()


if __name__ == '__main__':
    run_script(sys.argv[1])