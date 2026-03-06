class Token:
    
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, line={self.line}, col={self.column})'

INT      = 'INT'
BOOL     = 'BOOL'
ID       = 'ID'

LET      = 'LET'
REC      = 'REC'
IN       = 'IN'
IF       = 'IF'
THEN     = 'THEN'
ELSE     = 'ELSE'
FUN      = 'FUN'
NOT      = 'NOT'

PLUS     = 'PLUS'
MINUS    = 'MINUS'
STAR     = 'STAR'
SLASH    = 'SLASH'

EQ       = 'EQ'
NEQ      = 'NEQ'
LT       = 'LT'
GT       = 'GT'
LEQ      = 'LEQ'
GEQ      = 'GEQ'

AND      = 'AND'
OR       = 'OR'

ARROW    = 'ARROW'
LPAREN   = 'LPAREN'
RPAREN   = 'RPAREN'
SEMISEMI = 'SEMISEMI'

EOF      = 'EOF'

KEYWORDS = {
    'let':   LET,
    'rec':   REC,
    'in':    IN,
    'if':    IF,
    'then':  THEN,
    'else':  ELSE,
    'fun':   FUN,
    'not':   NOT,
    'true':  BOOL,
    'false': BOOL,
}
