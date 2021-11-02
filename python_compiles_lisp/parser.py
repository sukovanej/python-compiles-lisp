from __future__ import annotations

from dataclasses import dataclass

from python_compiles_lisp.lexer import IntegerToken, NonValueToken, SymbolToken, Token, tokenize


@dataclass
class SyntaxTree:
    items: list[SyntaxTree | IntegerToken | SymbolToken]


Statement = SyntaxTree | IntegerToken | SymbolToken


def parse_string(input_string: str) -> list[Statement]:
    tokens = tokenize(input_string)
    return parse_tokens(tokens)


def parse_tokens(tokens: list[Token]) -> list[Statement]:
    statements = []
    n_of_tokens = len(tokens)
    idx = 0

    while idx < n_of_tokens:
        ast, idx = parse_token(idx, tokens)
        statements.append(ast)
        idx += 1

    return statements


def parse_list_statement(idx: int, tokens: list[Token]) -> tuple[Statement, int]:
    if tokens[idx] != NonValueToken.LEFT_PAR:
        raise ValueError(f"Expected NonValueToken.LEFT_PAR, got {tokens[idx]}")

    items = []
    idx += 1

    while tokens[idx] != NonValueToken.RIGHT_PAR:
        new_item, idx = parse_token(idx, tokens)
        items.append(new_item)
        idx += 1

    return SyntaxTree(items), idx


def parse_token(idx: int, tokens: list[Token]) -> tuple[Statement, int]:
    token = tokens[idx]

    if isinstance(token, IntegerToken) or isinstance(token, SymbolToken):
        return token, idx
    elif token == NonValueToken.LEFT_PAR:
        ast, idx = parse_list_statement(idx, tokens)
        return ast, idx
    else:
        raise Exception(f"Expected token {token}")
