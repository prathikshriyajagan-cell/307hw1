# Lexer and Parser for MiniML

## Executing the Code

```bash
python main.py <source_file>
```

Example:

### test1.ml
```bash
2 + 3 * 4
```

```bash
python main.py test1.ml
# BinaryOp('+', IntLiteral(2), BinaryOp('*', IntLiteral(3), IntLiteral(4)))
```
