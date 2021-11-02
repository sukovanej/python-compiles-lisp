from dataclasses import dataclass
from enum import Enum


@dataclass
class IntegerToken:
    value: int


@dataclass
class SymbolToken:
    value: str


class NonValueToken(Enum):
    LEFT_PAR = "("
    RIGHT_PAR = ")"


Token = IntegerToken | SymbolToken | NonValueToken


def convert_buffer_to_token(buffer: str) -> Token:
    if buffer.isnumeric():
        return IntegerToken(int(buffer))
    else:
        return SymbolToken(buffer)


def tokenize(input_string: str) -> list[Token]:
    tokens = []

    buffer = ""

    for c in input_string:
        if c == "(":
            tokens.append(NonValueToken.LEFT_PAR)
        elif c == ")":
            if buffer:
                tokens.append(convert_buffer_to_token(buffer))
                buffer = ""

            tokens.append(NonValueToken.RIGHT_PAR)
        elif c == " " and buffer:
            tokens.append(convert_buffer_to_token(buffer))
            buffer = ""
        elif c != " ":
            buffer += c

    if buffer:
        tokens.append(convert_buffer_to_token(buffer))

    return tokens
