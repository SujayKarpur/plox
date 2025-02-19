from typing import List
import re 
import sys 

from lox import tokens
from lox import state
from lox import utils 




class Lexer: 
    """
    Implementation of a lexer/scanner for plox

    Lexical Grammar:
    """

    def __init__(self, string : str):
        self.position : int = 0
        self.row : int = 0 
        self.column : int = 0
        self.string : str = string  
        self.MAX_POSITION : int = len(string)
        self.lexed_tokens : List[tokens.Token] = [] 


    def match_token(self):
        for tokentype in tokens.TokenType:
            pattern = re.compile(tokentype.value)
            match = pattern.match(self.string, pos=self.position)
            if match:
                matched_object = match.group()
                if tokentype == tokens.TokenType.IDENTIFIER:
                    if matched_object in state.KEYWORDS:
                        continue 
                new_token = tokens.Token(tokentype, matched_object, self.position, self.row, self.column)
                self.position += len(matched_object)
                self.column += len(matched_object)
                self.actions(new_token)
                return new_token


    def actions(self, token: tokens.Token) -> None:
        match token.type:
            case tokens.TokenType.NEWLINE:
                self.row += 1 
                self.column = 0
            case tokens.TokenType.STRING:
                token.value = token.value[1:-1]
            case tokens.TokenType.NUMBER:
                token.value = float(token.value)
            case tokens.TokenType.UNRECOGNIZABLE:
                self.report(f"Invalid character : {token.value}")
            case _: 
                pass 


    def lex(self):

        while self.position < self.MAX_POSITION:
            new_token = self.match_token()
            self.lexed_tokens.append(new_token)

        self.lexed_tokens = list(filter(lambda i : i.type not in tokens.IGNORED_TOKENS, self.lexed_tokens)) 

        return self.lexed_tokens 
    

    def report(self, message : str) -> None:
        
        print(f"file {state.current_file_name}, line {self.row+1}, column {self.column}")
        print(f"{utils.nth_line_of_string(state.currently_executing_program, self.row)}")
        print(" " * (self.column-1) + "^")
        print(f"LexError: {message}")
        state.error_flag = True 
        sys.exit()
