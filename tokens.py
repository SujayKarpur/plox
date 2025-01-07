import errors 
import re 
import enum 

KEYWORDS = {'and', 'class', 'else', 'false', 'fun', 'for', 'if', 'nil', 'or', 'print', 'return', 'scan', 'super', 'this', 'true', 'var', 'while'}
#global vars: 
lexer_row = lexer_column = 0

class TokenType(enum.Enum):
    #EOF = 0 
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
    STRING = r'"([^\\]*(\\(\\|n|t|\"))?[^\\]*)+"' 
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
                    if matched_object in KEYWORDS:
                        continue 
                new_token = Token(tokentype, matched_object, position, row, column)
                return (new_token, len(matched_object))



class Token: 

    def __init__(self, tokentype: TokenType, matched_object: str, position: int, row: int, column: int, ): 
        self.type = tokentype.name 
        self.value = matched_object
        self.position = position
        self.row = row 
        self.column = column
        actions(self) 

    def __repr__(self) -> str:
        return f"({self.type} , {self.value})" 




def actions(token: Token) -> None:
    global lexer_row, lexer_column
    match token.type:
        case TokenType.NEWLINE.name:
            lexer_column = 0
            lexer_row += 1
        case TokenType.STRING.name:
            token.value = token.value[1:-1]
        case TokenType.NUMBER.name:
            token.value = float(token.value)
        case TokenType.UNRECOGNIZABLE.name:
            errors.error(lexer_row, f"unexpected character : {token.value}")
        case _: 
            pass 
