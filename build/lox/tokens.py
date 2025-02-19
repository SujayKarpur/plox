import enum 
import operator
import typing 
import dataclasses

from lox import state 
from lox import errors 

class TokenType(enum.Enum):

    #comments
    COMMENT = r'//.*\n'
    MULTI_LINE_COMMENT = r'/\*(.|\n)*\*/'

    #punctuation
    LEFT_PAREN = r'\('
    RIGHT_PAREN = r'\)'
    LEFT_BRACE = r'\{'
    RIGHT_BRACE = r'\}'
    SEMICOLON = r';'
    COMMA = r','
    LEFT_SQUARE = r'\['
    RIGHT_SQUARE = r'\]'

    #operators
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
    QUESTION = r'\?'
    COLON = r':'

    #literals/identifiers
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*' 
    STRING = r'"([^\\\"]*(\\(\\|n|t|\"))?[^\\\"]*)+"' 
    NUMBER = r'[0-9]+(\.[0-9]+)?' 
    LIST = r'\[\]'

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
    RETURN = r'return'
    SUPER = r'super'
    THIS = r'this'
    TRUE = r'true' 
    VAR = r'var' 
    WHILE = r'while'
    EACH = r'each'
    IN = r'in'


    #whitespace
    SPACE = r'\s'
    TAB = r'\t'
    NEWLINE = r'\n'

    #error
    UNRECOGNIZABLE = r'(.|\n)+?'




class Token: 

    def __init__(self, tokentype: TokenType, matched_object: str, position: int, row: int, column: int): 
        self.type = tokentype 
        self.value = matched_object
        self.position = position
        self.row = row 
        self.column = column

    def __repr__(self) -> str:
        return f"({self.type.name} , {self.value})" 






def safify(fun : typing.Callable) -> typing.Callable:
    if fun in {operator.add, operator.sub, operator.truediv}:
        return lambda a, b : fun(a,b) if (type(a) == type(b)) else errors.report("RuntimeError", state.current_file_name, 1,1, f"Can't {a} {b}")
    elif fun in {operator.mul}:
        return lambda a, b : fun(int(a),b) if (type(a) == float) else (fun(a,int(b)) if (type(b) == float) else errors.report("RuntimeError", state.current_file_name, 1,1, f"Can't {a} {b}"))
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
                        TokenType.LIST
                  }

LITERAL_CONSTANTS = {
                        TokenType.TRUE : True, 
                        TokenType.FALSE : False,
                        TokenType.NIL : None 
                    }

IGNORED_TOKENS = {TokenType.COMMENT, TokenType.MULTI_LINE_COMMENT, TokenType.SPACE, TokenType.NEWLINE, TokenType.TAB}


