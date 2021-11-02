from dataclasses import dataclass
from typing import Callable

from python_compiles_lisp.lexer import IntegerToken, SymbolToken
from python_compiles_lisp.parser import Statement, SyntaxTree, parse_string
from python_compiles_lisp.compile import CompilerInstruction


Value = int
Function = Callable[..., int]

ProgramStack = list[Value]

Memory = dict[str, list[int]]


def evaluate_string(input_string: str) -> None:
    statements = parse_string(input_string)
    evaluate(statements)


def evaluate(statements: list[Statement]) -> None:
    stack = []

    for statement in statements:
        evaluate_statement(stack, statement)


def evaluate_statement(stack: ProgramStack, statement: Statement) -> Value:
    match statement:
        case IntegerToken(value=value):
            return value
        case SymbolToken(value=symbol):
            return evaluate_symbol(symbol)
        case SyntaxTree(items=items):
            evaluated_items = [evaluate_statement(stack, s) for s in items]
            function = evaluated_items.pop(0)

            if not callable(function):
                raise Exception(f"Expected callable, got {function}")

            return function(*evaluated_items)

    raise ValueError(f"Unexpected statement {statement}")


def evaluate_symbol(symbol: str) -> Value:
    functions = {
        "sys-call": evaluate_sys_call,
        "push": evaluate_push,
        "pop": evaluate_pop,
        "~stack-pointer": CompilerInstruction.STACK_POINTER,
    }

    if symbol in functions:
        return functions[symbol]

    raise Exception(f"unknown symbol {symbol}")


def evaluate_push(memory: Memory, value: Value) -> None:
    memory.stack.append(value)


def evaluate_pop(memory: Memory) -> Value:
    return memory.stack.pop()


def evaluate_sys_call(memory: Memory, eax, ebx, ecx = None, edx = None) -> Value:
    match eax:
        case 1: # sys_exit
            exit(ebx)
        case 4: # sys_write
            if ebx == 1: # stdout
                print()
            else:
                raise NotImplementedError("syscall - unknown file descriptor {ebx}")
        case _:
            raise NotImplementedError(f"syscall - unknown syscall {eax}")
