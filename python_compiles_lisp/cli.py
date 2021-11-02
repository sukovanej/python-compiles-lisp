import sys
from pprint import pprint

from .lexer import tokenize
from .parser import parse_string
from .evaluate import evaluate_string


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0]
    filename = args[1]

    match cmd:
        case "i":
            with open(filename) as f:
                evaluate_string(f.read())
        case "lex":
            with open(filename) as f:
                pprint(tokenize(f.read()))
        case "ast":
            with open(filename) as f:
                pprint(parse_string(f.read()))
        case c:
            raise ValueError(f"Command {c} not known")
