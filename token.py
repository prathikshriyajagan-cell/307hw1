class Token:
    """Represents a single token produced by the lexer."""

    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, line={self.line}, col={self.column})'


# Token type constants
INT      = 'INT'
BOOL     = 'BOOL'
ID       = 'ID'

# Keywords
LET      = 'LET'
REC      = 'REC'
IN       = 'IN'
IF       = 'IF'
THEN     = 'THEN'
ELSE     = 'ELSE'
FUN      = 'FUN'
NOT      = 'NOT'

# Arithmetic operators
PLUS     = 'PLUS'
MINUS    = 'MINUS'
STAR     = 'STAR'
SLASH    = 'SLASH'

# Comparison operators
EQ       = 'EQ'
NEQ      = 'NEQ'
LT       = 'LT'
GT       = 'GT'
LEQ      = 'LEQ'
GEQ      = 'GEQ'

# Boolean operators
AND      = 'AND'
OR       = 'OR'

# Other operators / delimiters
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
