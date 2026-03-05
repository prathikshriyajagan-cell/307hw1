class IntLiteral:
    def __init__(self, value):
        self.value = value  # int

    def __repr__(self):
        return f'IntLiteral({self.value})'


class BoolLiteral:
    def __init__(self, value):
        self.value = value  # bool

    def __repr__(self):
        return f'BoolLiteral({self.value})'


class Variable:
    def __init__(self, name):
        self.name = name  # str

    def __repr__(self):
        return f'Variable({self.name!r})'


class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op        # str, e.g. '+', '&&'
        self.left = left
        self.right = right

    def __repr__(self):
        return f'BinaryOp({self.op!r}, {self.left!r}, {self.right!r})'


class UnaryOp:
    def __init__(self, op, operand):
        self.op = op        # 'not' or '-'
        self.operand = operand

    def __repr__(self):
        return f'UnaryOp({self.op!r}, {self.operand!r})'


class Let:
    """
    Represents both simple let bindings and function shorthand.

    let [rec] name params... = bound_expr in body_expr
    """

    def __init__(self, name, params, bound_expr, body_expr, is_rec=False):
        self.name = name            # str
        self.params = params        # list[str], empty for simple bindings
        self.bound_expr = bound_expr
        self.body_expr = body_expr
        self.is_rec = is_rec        # bool

    def __repr__(self):
        rec = 'rec ' if self.is_rec else ''
        params = (' ' + ' '.join(self.params)) if self.params else ''
        return (
            f'Let({rec}{self.name!r}{params}, '
            f'{self.bound_expr!r}, {self.body_expr!r})'
        )


class If:
    def __init__(self, condition, then_expr, else_expr):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

    def __repr__(self):
        return f'If({self.condition!r}, {self.then_expr!r}, {self.else_expr!r})'


class Fun:
    """Anonymous function: fun param1 param2 ... -> body"""

    def __init__(self, params, body):
        self.params = params    # list[str], at least one
        self.body = body

    def __repr__(self):
        return f'Fun({self.params!r}, {self.body!r})'


class App:
    """Function application: func arg"""

    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f'App({self.func!r}, {self.arg!r})'
