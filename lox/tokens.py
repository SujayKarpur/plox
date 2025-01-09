import re 
import enum 
import operator
import typing 

from lox import state 
from lox import errors 

class TokenType(enum.Enum):

    COMMENT = r'//.*\n'
    MULTI_LINE_COMMENT = r'/\*(.|\n)*\*/'

    LEFT_PAREN = r'\('
    RIGHT_PAREN = r'\)'
    LEFT_BRACE = r'\{'
    RIGHT_BRACE = r'\}'
    SEMICOLON = r';'
    COMMA = r','

    DOT = r'\.'
    PLUS = r'\+'
    MINUS = r'-' 
    TIMES = r'\*'
    DIVIDED_BY = r'/'
    BANG_EQUAL = r'!='
    BANG = r'!'
    EQUAL_EQUAL = r'=='
    EQUAL = r'='
    GREATER_EQUAL = r'>=' 
    GREATER = r'>'
    LESSER_EQUAL = r'<='
    LESSER = r'<'

    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*' 
    STRING = r'"([^\\\"]*(\\(\\|n|t|\"))?[^\\\"]*)+"' 
    NUMBER = r'[0-9]+(\.[0-9]+)?' 
    #ARRAY = r''

    #keywords
    AND = r'and'
    CLASS = r'class'
    ELSE = r'else'
    FALSE = r'false'
    FUN = r'fun' 
    FOR = r'for' 
    IF = r'if' 
    NIL = r'nil' 
    OR = r'or'
    PRINT = r'print'
    RETURN = r'return'
    SCAN = r'scan'
    SUPER = r'super'
    THIS = r'this'
    TRUE = r'true' 
    VAR = r'var' 
    WHILE = r'while'



    SPACE = r'\s'
    TAB = r'\t'
    NEWLINE = r'\n'

    UNRECOGNIZABLE = r'(.|\n)+?'

    @staticmethod
    def match(string, position, row, column):
        for tokentype in TokenType:
            pattern = re.compile(tokentype.value)
            match = pattern.match(string, pos=position)
            if match:
                matched_object = match.group()
                if tokentype == TokenType.IDENTIFIER:
                    if matched_object in state.KEYWORDS:
                        continue 
                new_token = Token(tokentype, matched_object, position, row, column)
                return (new_token, len(matched_object))



class Token: 

    def __init__(self, tokentype: TokenType, matched_object: str, position: int, row: int, column: int): 
        self.type = tokentype 
        self.value = matched_object
        self.position = position
        self.row = row 
        self.column = column
        actions(self) 

    def __repr__(self) -> str:
        return f"({self.type.name} , {self.value})" 




def actions(token: Token) -> None:
    match token.type:
        case TokenType.NEWLINE:
            state.reset_lexer(state.lexer_position, state.lexer_row+1, 0)
        case TokenType.STRING:
            token.value = token.value[1:-1]
        case TokenType.NUMBER:
            token.value = float(token.value)
        case TokenType.UNRECOGNIZABLE:
            errors.report("LexError", state.current_file_name, state.lexer_row, state.lexer_column, f"Invalid character : {token.value}")
        case _: 
            pass 


def safify(fun : typing.Callable) -> typing.Callable:
    if fun in {operator.add, operator.sub, operator.mul, operator.truediv}:
        return lambda a, b : fun(a,b) if (type(a) == type(b) == float) else errors.report("RuntimeError", state.current_file_name, 1,1, f"Can't {a} {b}")
    else:
        return lambda a, b : fun(a,b) if (type(a) == type(b)) else errors.report("RuntimeError", state.current_file_name, 1,1, "Can't ")

OPERATIONS = {
                TokenType.PLUS: safify(operator.add),
                TokenType.MINUS: safify(operator.sub),
                TokenType.TIMES: safify(operator.mul),
                TokenType.DIVIDED_BY: safify(operator.truediv),
                TokenType.EQUAL_EQUAL: safify(operator.eq),
                TokenType.BANG_EQUAL: safify(lambda x,y : x != y), 
                TokenType.GREATER: safify(operator.gt), 
                TokenType.GREATER_EQUAL: safify(operator.ge), 
                TokenType.LESSER: safify(operator.lt),
                TokenType.LESSER_EQUAL: safify(operator.le),
             }   

UNARY_OPERATORS = {
            TokenType.MINUS,
            TokenType.BANG
        }

EQUALITY_OPERATORS = {
                TokenType.EQUAL_EQUAL, 
                TokenType.BANG_EQUAL
           }

COMPARISON_OPERATORS = {
                            TokenType.GREATER, 
                            TokenType.GREATER_EQUAL, 
                            TokenType.LESSER, 
                            TokenType.LESSER_EQUAL
                       }

LITERAL_OBJECTS = {
                        TokenType.NUMBER, 
                        TokenType.STRING, 
                        TokenType.IDENTIFIER
                  }

LITERAL_CONSTANTS = {
                        TokenType.TRUE : True, 
                        TokenType.FALSE : False,
                        TokenType.NIL : None 
                    }