import pytest

from python_compiles_lisp.lexer import IntegerToken, NonValueToken, SymbolToken, Token
from python_compiles_lisp.parser import SyntaxTree, parse_string

LP, RP, S, I, ST = (
    NonValueToken.LEFT_PAR,
    NonValueToken.RIGHT_PAR,
    SymbolToken,
    IntegerToken,
    SyntaxTree,
)


@pytest.mark.parametrize(
    "input_string, syntax_tree",
    [
        ("+", [S("+")]),
        (" +", [S("+")]),
        ("+ ", [S("+")]),
        (" + ", [S("+")]),
        ("123", [I(123)]),
        ("123 ", [I(123)]),
        (" 123", [I(123)]),
        (" 123 ", [I(123)]),
        ("(hello world)", [ST([S("hello"), S("world")])]),
        ("(hello (1 world (+ 69 69)))", [ST([S("hello"), ST([I(1), S("world"), ST([S("+"), I(69), I(69)])])])]),
    ],
)
def test_parse_string(input_string: str, syntax_tree: list[Token]) -> None:
    assert parse_string(input_string) == syntax_tree
