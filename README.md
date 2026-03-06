# Lexer and Parser for MiniML

A lexical analyzer and recursive-descent parser for MiniML, a simplified subset of OCaml.

## Files

| File | Description |
|---|---|
| `token.py` | Token class and token type constants |
| `lexer.py` | Lexical analyzer — converts source code to tokens |
| `ast_nodes.py` | AST node class definitions |
| `parser.py` | Recursive-descent parser — converts tokens to an AST |
| `main.py` | CLI driver |

## Requirements

- Python 3.10 or higher
- No external libraries required (standard library only)

## Executing the Code

1. Clone or download this repository.
2. Navigate to the project directory:
   ```bash
   cd 307hw1
   ```
3. Run the program by passing a MiniML source file as an argument:
   ```bash
   python3 main.py <source_file>
   ```
   The program will print the AST of the parsed expression to stdout. Errors are printed to stderr.

**Example:**

```bash
python3 main.py tests/test1.ml
# Output: BinaryOp('+', IntLiteral(2), BinaryOp('*', IntLiteral(3), IntLiteral(4)))
```

You can also write your own `.ml` file and pass it:

```bash
echo "let x = 42 in x + 1" > my_prog.ml
python3 main.py my_prog.ml
# Output: Let('x', IntLiteral(42), BinaryOp('+', Variable('x'), IntLiteral(1)))
```

## Language Features

- **Integer literals**: `0`, `42`, `123`
- **Boolean literals**: `true`, `false`
- **Arithmetic**: `+`, `-`, `*`, `/` (standard precedence, left-associative)
- **Comparison**: `=`, `<>`, `<`, `>`, `<=`, `>=`
- **Boolean operators**: `&&`, `||` (left-associative), `not` (unary)
- **Unary minus**: `-x`
- **Let bindings**: `let x = 5 in x + 1`
- **Recursive definitions**: `let rec f n = ... in f 5`
- **Multi-parameter functions**: `let add x y = x + y in add 3 4`
- **Anonymous functions**: `fun x -> x + 1`
- **Function application**: `f x`, `f (x + 1)`
- **Conditionals**: `if cond then e1 else e2`
- **Parenthesized expressions**: `(2 + 3) * 4`
- **Comments**: `(* this is a comment *)`

## Grammar

```
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
```

## AST Nodes

| Node | Fields | Example output |
|---|---|---|
| `IntLiteral` | `exp` | `IntLiteral(42)` |
| `BoolLiteral` | `exp` | `BoolLiteral(True)` |
| `Variable` | `title` | `Variable('x')` |
| `BinaryOp` | `op`, `leftward`, `rightward` | `BinaryOp('+', ..., ...)` |
| `UnaryOp` | `op`, `operand` | `UnaryOp('-', ...)` |
| `Let` | `name`, `params`, `bound_expr`, `body_expr`, `is_rec` | `Let('x', ..., ...)` |
| `If` | `condition`, `then_expr`, `else_expr` | `If(..., ..., ...)` |
| `Fun` | `params`, `body` | `Fun(['x'], ...)` |
| `App` | `func`, `arg` | `App(..., ...)` |

## Error Handling

Lexical and syntax errors include the line and column number:

```
Lexical Error at line 1, col 5: unrecognized character '@'
Syntax Error at line 1, col 10: expected THEN, got ID ('x')
Lexical Error at line 1, col 1: unterminated comment
```

## Tests

Eight test cases are provided in the `tests/` directory:

| File | Expression |
|---|---|
| `test1.ml` | `2 + 3 * 4` |
| `test2.ml` | `let x = 5 in x + 1` |
| `test3.ml` | `if x < 0 then -x else x` |
| `test4.ml` | `let f = fun x -> x + 1 in f 5` |
| `test5.ml` | `let rec factorial n = if n = 0 then 1 else n * factorial (n - 1) in factorial 5` |
| `test6.ml` | `let add x y = x + y in add 3 4` |
| `test7.ml` | `(true && false) \|\| not false` |
| `test8.ml` | `let rec power x n = if n = 0 then 1 else x * power x (n - 1) in power 2 8` |

Run all tests:

```bash
for i in 1 2 3 4 5 6 7 8; do echo "=== Test $i ==="; python3 main.py tests/test$i.ml; done
```
