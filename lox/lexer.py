from typing import List
import re 

from lox import tokens
from lox import state
from lox import errors




class Lexer: 


    def __init__(self):
        self.position : int = 0
        self.row : int = 0 
        self.column : int = 0 


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
                errors.report("LexError", state.current_file_name, state.lexer_row, state.lexer_column, f"Invalid character : {token.value}")
            case _: 
                pass 


    def lex(self, string : str):

        self.string : str = string  
        self.MAX_POSITION : int = len(string)
        self.lexed_tokens : List[tokens.Token] = []

        while self.position < self.MAX_POSITION:
            new_token = self.match_token()
            self.lexed_tokens.append(new_token)

        
        self.lexed_tokens = list(filter(lambda i : i.type not in tokens.IGNORED_TOKENS, self.lexed_tokens)) 

        return self.lexed_tokens 
