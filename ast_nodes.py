class IntLiteral:
    def __init__(self, value):
        self.exp = value  # int

    def __repr__(self):
        return f'IntLiteral({self.exp})'


class BoolLiteral:
    def __init__(self, value):
        self.exp = value 

    def __repr__(self):
        return f'BoolLiteral({self.value})'


class Variable:
    def __init__(self, name):
        self.title = name 

    def __repr__(self):
        return f'Variable({self.name!r})'


class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.leftward = left
        self.rightward = right

    def __repr__(self):
        return f'BinaryOp({self.op!r}, {self.leftward!r}, {self.rightward!r})'


class UnaryOp:
    def __init__(self, op, operand):
        self.op = op  
        self.operand = operand

    def __repr__(self):
        return f'UnaryOp({self.op!r}, {self.operand!r})'


class Let:

    def __init__(self, name, params, bound_expr, body_expr, is_rec=False):
        self.name = name       
        self.params = params        
        self.bound_expr = bound_expr
        self.body_expr = body_expr
        self.is_rec = is_rec  

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
    def __init__(self, params, body):
        self.params = params 
        self.body = body

    def __repr__(self):
        return f'Fun({self.params!r}, {self.body!r})'


class App:
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f'App({self.func!r}, {self.arg!r})'
