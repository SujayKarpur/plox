from typing import Protocol

class LoxCallable(Protocol): 

    def call(interpreter, arguments): 
        pass 

    def arity() -> int:
        pass 