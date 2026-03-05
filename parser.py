import token as T
from ast_nodes import (
    IntLiteral, BoolLiteral, Variable,
    BinaryOp, UnaryOp, Let, If, Fun, App,
)


class ParseError(Exception):
    pass


class Parser:
    """
    Recursive-descent parser for MiniML.

    Grammar:
        program     -> expr
        expr        -> let_expr | if_expr | fun_expr | or_expr
        let_expr    -> LET [REC] ID [ID]* = expr IN expr
        if_expr     -> IF expr THEN expr ELSE expr
        fun_expr    -> FUN ID [ID]* -> expr
        or_expr     -> and_expr (|| and_expr)*
        and_expr    -> comp_expr (&& comp_expr)*
        comp_expr   -> add_expr [comp_op add_expr]
        comp_op     -> = | <> | < | > | <= | >=
        add_expr    -> mult_expr ((+ | -) mult_expr)*
        mult_expr   -> unary_expr ((* | /) unary_expr)*
        unary_expr  -> (NOT | -) unary_expr | app_expr
        app_expr    -> primary_expr primary_expr*
        primary_expr -> INT | BOOL | ID | ( expr )
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def current(self):
        return self.tokens[self.pos]

    def peek(self, offset=1):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # EOF

    def advance(self):
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def expect(self, tok_type):
        tok = self.current()
        if tok.type != tok_type:
            if tok.type == T.EOF:
                raise ParseError(
                    f'Syntax Error at line {tok.line}, col {tok.column}: '
                    f'unexpected end of input, expected {tok_type}'
                )
            raise ParseError(
                f'Syntax Error at line {tok.line}, col {tok.column}: '
                f"expected {tok_type}, got {tok.type} ({tok.value!r})"
            )
        return self.advance()

    def error(self, msg):
        tok = self.current()
        raise ParseError(
            f'Syntax Error at line {tok.line}, col {tok.column}: {msg}'
        )

    def at(self, *types):
        return self.current().type in types

    # ------------------------------------------------------------------
    # Primary start-set: tokens that can begin a primary_expr
    # ------------------------------------------------------------------

    PRIMARY_FIRST = {T.INT, T.BOOL, T.ID, T.LPAREN}

    # ------------------------------------------------------------------
    # Grammar rules
    # ------------------------------------------------------------------

    def parse_program(self):
        node = self.parse_expr()
        # optional terminator
        if self.at(T.SEMISEMI):
            self.advance()
        if not self.at(T.EOF):
            self.error(f"unexpected token {self.current().type} ({self.current().value!r})")
        return node

    # expr -> let_expr | if_expr | fun_expr | or_expr
    def parse_expr(self):
        if self.at(T.LET):
            return self.parse_let_expr()
        if self.at(T.IF):
            return self.parse_if_expr()
        if self.at(T.FUN):
            return self.parse_fun_expr()
        return self.parse_or_expr()

    # let_expr -> LET [REC] ID [ID]* = expr IN expr
    def parse_let_expr(self):
        self.expect(T.LET)
        is_rec = False
        if self.at(T.REC):
            self.advance()
            is_rec = True

        name_tok = self.expect(T.ID)
        name = name_tok.value

        # Collect optional parameter names
        params = []
        while self.at(T.ID):
            params.append(self.advance().value)

        self.expect(T.EQ)
        bound = self.parse_expr()
        self.expect(T.IN)
        body = self.parse_expr()
        return Let(name, params, bound, body, is_rec)

    # if_expr -> IF expr THEN expr ELSE expr
    def parse_if_expr(self):
        self.expect(T.IF)
        cond = self.parse_expr()
        self.expect(T.THEN)
        then_e = self.parse_expr()
        self.expect(T.ELSE)
        else_e = self.parse_expr()
        return If(cond, then_e, else_e)

    # fun_expr -> FUN ID [ID]* -> expr
    def parse_fun_expr(self):
        self.expect(T.FUN)
        params = []
        if not self.at(T.ID):
            self.error("expected parameter name after 'fun'")
        while self.at(T.ID):
            params.append(self.advance().value)
        self.expect(T.ARROW)
        body = self.parse_expr()
        return Fun(params, body)

    # or_expr -> and_expr (|| and_expr)*
    def parse_or_expr(self):
        node = self.parse_and_expr()
        while self.at(T.OR):
            self.advance()
            right = self.parse_and_expr()
            node = BinaryOp('||', node, right)
        return node

    # and_expr -> comp_expr (&& comp_expr)*
    def parse_and_expr(self):
        node = self.parse_comp_expr()
        while self.at(T.AND):
            self.advance()
            right = self.parse_comp_expr()
            node = BinaryOp('&&', node, right)
        return node

    COMP_OPS = {T.EQ, T.NEQ, T.LT, T.GT, T.LEQ, T.GEQ}

    # comp_expr -> add_expr [comp_op add_expr]
    def parse_comp_expr(self):
        node = self.parse_add_expr()
        if self.at(*self.COMP_OPS):
            op_tok = self.advance()
            right = self.parse_add_expr()
            node = BinaryOp(op_tok.value, node, right)
        return node

    # add_expr -> mult_expr ((+ | -) mult_expr)*
    def parse_add_expr(self):
        node = self.parse_mult_expr()
        while self.at(T.PLUS, T.MINUS):
            op_tok = self.advance()
            right = self.parse_mult_expr()
            node = BinaryOp(op_tok.value, node, right)
        return node

    # mult_expr -> unary_expr ((* | /) unary_expr)*
    def parse_mult_expr(self):
        node = self.parse_unary_expr()
        while self.at(T.STAR, T.SLASH):
            op_tok = self.advance()
            right = self.parse_unary_expr()
            node = BinaryOp(op_tok.value, node, right)
        return node

    # unary_expr -> (NOT | -) unary_expr | app_expr
    def parse_unary_expr(self):
        if self.at(T.NOT):
            self.advance()
            operand = self.parse_unary_expr()
            return UnaryOp('not', operand)
        if self.at(T.MINUS):
            self.advance()
            operand = self.parse_unary_expr()
            return UnaryOp('-', operand)
        return self.parse_app_expr()

    # app_expr -> primary_expr primary_expr*
    def parse_app_expr(self):
        func = self.parse_primary_expr()
        while self.at(*self.PRIMARY_FIRST):
            arg = self.parse_primary_expr()
            func = App(func, arg)
        return func

    # primary_expr -> INT | BOOL | ID | ( expr )
    def parse_primary_expr(self):
        tok = self.current()

        if tok.type == T.INT:
            self.advance()
            return IntLiteral(int(tok.value))

        if tok.type == T.BOOL:
            self.advance()
            return BoolLiteral(tok.value == 'true')

        if tok.type == T.ID:
            self.advance()
            return Variable(tok.value)

        if tok.type == T.LPAREN:
            self.advance()
            node = self.parse_expr()
            self.expect(T.RPAREN)
            return node

        if tok.type == T.EOF:
            raise ParseError(
                f'Syntax Error at line {tok.line}, col {tok.column}: '
                f'unexpected end of input'
            )
        raise ParseError(
            f'Syntax Error at line {tok.line}, col {tok.column}: '
            f"unexpected token {tok.type} ({tok.value!r})"
        )


def parse(tokens):
    return Parser(tokens).parse_program()
