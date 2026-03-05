from token import Token, KEYWORDS
import token as T


class LexerError(Exception):
    pass


class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def error(self, msg):
        raise LexerError(f'Lexical Error at line {self.line}, col {self.column}: {msg}')

    def current(self):
        if self.position < len(self.source):
            return self.source[self.pos]
        return None

    def peek(self, offset=1):
        idx = self.position + offset
        if idx < len(self.source):
            return self.source[idx]
        return None

    def advance(self):
        ch = self.source[self.position]
        self.position += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace(self):
        while self.current() is not None and self.current() in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        """Skip (* ... *) style comments."""
        start_line = self.line
        start_col = self.column
        # consume (*
        self.advance()  # (
        self.advance()  # *
        while self.current() is not None:
            if self.current() == '*' and self.peek() == ')':
                self.advance()  # *
                self.advance()  # )
                return
            self.advance()
        raise LexerError(
            f'Lexical Error at line {start_line}, col {start_col}: unterminated comment'
        )

    def read_int(self):
        start_col = self.column
        digits = []
        while self.current() is not None and self.current().isdigit():
            digits.append(self.advance())
        return Token(T.INT, ''.join(digits), self.line, start_col)

    def read_id_or_keyword(self):
        start_col = self.column
        chars = []
        while self.current() is not None and (
            self.current().isalnum() or self.current() == '_'
        ):
            chars.append(self.advance())
        word = ''.join(chars)
        tok_type = KEYWORDS.get(word, T.ID)
        return Token(tok_type, word, self.line, start_col)

    def make_token(self, tok_type, value):
        return Token(tok_type, value, self.line, self.column)

    def tokenize(self):
        while True:
            self.skip_whitespace()
            ch = self.current()

            if ch is None:
                self.tokens.append(Token(T.EOF, '', self.line, self.column))
                break

            # Comments
            if ch == '(' and self.peek() == '*':
                self.skip_comment()
                continue

            # Integer literals
            if ch.isdigit():
                self.tokens.append(self.read_int())
                continue

            # Identifiers and keywords
            if ch.islower():
                self.tokens.append(self.read_id_or_keyword())
                continue

            # Two-character operators
            if ch == '<' and self.peek() == '=':
                tok = self.make_token(T.LEQ, '<=')
                self.advance(); self.advance()
                self.tokens.append(tok)
                continue

            if ch == '>' and self.peek() == '=':
                tok = self.make_token(T.GEQ, '>=')
                self.advance(); self.advance()
                self.tokens.append(tok)
                continue

            if ch == '<' and self.peek() == '>':
                tok = self.make_token(T.NEQ, '<>')
                self.advance(); self.advance()
                self.tokens.append(tok)
                continue

            if ch == '&' and self.peek() == '&':
                tok = self.make_token(T.AND, '&&')
                self.advance(); self.advance()
                self.tokens.append(tok)
                continue

            if ch == '|' and self.peek() == '|':
                tok = self.make_token(T.OR, '||')
                self.advance(); self.advance()
                self.tokens.append(tok)
                continue

            if ch == '-' and self.peek() == '>':
                tok = self.make_token(T.ARROW, '->')
                self.advance(); self.advance()
                self.tokens.append(tok)
                continue

            if ch == ';' and self.peek() == ';':
                tok = self.make_token(T.SEMISEMI, ';;')
                self.advance(); self.advance()
                self.tokens.append(tok)
                continue

            # Single-character operators and delimiters
            single = {
                '+': T.PLUS,
                '-': T.MINUS,
                '*': T.STAR,
                '/': T.SLASH,
                '=': T.EQ,
                '<': T.LT,
                '>': T.GT,
                '(': T.LPAREN,
                ')': T.RPAREN,
            }
            if ch in single:
                tok = self.make_token(single[ch], ch)
                self.advance()
                self.tokens.append(tok)
                continue

            self.error(f"unrecognized character '{ch}'")

        return self.tokens


def tokenize(source):
    return Lexer(source).tokenize()
