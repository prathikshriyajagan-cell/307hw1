import sys
from lexer import tokenize, LexerError
from parser import parse, ParseError


def main():
    if len(sys.argv) != 2:
        print('Usage: python main.py <source_file>', file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            source = f.read()
    except FileNotFoundError:
        print(f'Error: file not found: {filename}', file=sys.stderr)
        sys.exit(1)

    try:
        tokens = tokenize(source)
    except LexerError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        ast = parse(tokens)
    except ParseError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    print(repr(ast))


if __name__ == '__main__':
    main()
