import pytest

from python_compiles_lisp.lexer import IntegerToken, NonValueToken, SymbolToken, Token, tokenize

LP, RP, S, I = (
    NonValueToken.LEFT_PAR,
    NonValueToken.RIGHT_PAR,
    SymbolToken,
    IntegerToken,
)


@pytest.mark.parametrize(
    "input_string, tokens",
    [
        ("+", [S("+")]),
        (" +", [S("+")]),
        ("+ ", [S("+")]),
        (" + ", [S("+")]),
        ("123", [I(123)]),
        ("123 ", [I(123)]),
        (" 123", [I(123)]),
        (" 123 ", [I(123)]),
        ("(hello world)", [LP, S("hello"), S("world"), RP]),
        (
            "(hello (1 world (+ 69 69)))",
            [LP, S("hello"), LP, I(1), S("world"), LP, S("+"), I(69), I(69), RP, RP, RP],
        ),
    ],
)
def test_tokenize(input_string: str, tokens: list[Token]) -> None:
    assert tokenize(input_string) == tokens
