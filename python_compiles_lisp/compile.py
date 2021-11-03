from typing import Callable
from python_compiles_lisp.lexer import IntegerToken, SymbolToken
from .parser import Statement, SyntaxTree, parse_string


DEFAULT_TEMPLATE = """
section .text
   global _start
	
_start:
{}

   ; Exit code
   mov eax, 1
   mov ebx, 0
   int 80h
"""


def compile_string(input_string: str) -> str:
    statements = parse_string(input_string)
    asm = ""

    for statement in statements:
        asm += create_asm(statement)

    return asm


def create_asm(statement: Statement) -> str | Callable[..., str] | :
    if isinstance(statement, IntegerToken):
        return str(statement.value)
    elif isinstance(statement, SymbolToken):
        return create_symbol_asm(statement.value)
    elif isinstance(statement, SyntaxTree):

        pass

    raise NotImplemented


def create_symbol_asm(symbol: str) -> Callable[..., str]:
    return FUNCTIONS[symbol]


def function_push(value: str):
    return f"push {value}"


def function_sub(left: str, right: str) -> tuple[str, str]:
    asm = f"mov eax, {left}\nmov ebx, {right}\nsub eax, ebx"
    return (asm, "eax")


FUNCTIONS = {
    "push": function_push,
    "-": function_sub,
}
