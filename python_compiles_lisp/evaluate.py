from typing import Callable
from functools import partial

from .lexer import IntegerToken, SymbolToken
from .parser import Statement, SyntaxTree, parse_string


Value = int
Function = Callable[..., int]


class Memory:
    # dummy memory model implementation
    def __init__(self) -> None:
        self._stack_max_capacity = 1000

        self._stack = []
        self._heap = []

        self._stack_pointer = -1

    @property
    def stack_pointer(self) -> int:
        return self._stack_pointer

    def access(self, pointer: int) -> int:
        if pointer < self._stack_max_capacity:
            return self._stack[pointer]
        else:
            return self._heap[pointer]

    def set(self, pointer: int, value: int) -> None:
        if pointer < self._stack_max_capacity:
            self._stack[pointer] = value
        else:
            self._heap[pointer] = value

    def push_stack(self, value: int) -> None:
        if self._stack_pointer == self._stack_max_capacity - 1:
            raise ValueError("Stack full")

        self._stack.append(value)
        self._stack_pointer += 1

    def pop_stack(self) -> int:
        if self._stack_pointer == 0:
            raise ValueError("Stack empty")

        self._stack_pointer -= 1
        return self._stack.pop()



def evaluate_string(input_string: str) -> None:
    statements = parse_string(input_string)
    evaluate(statements)


def evaluate(statements: list[Statement]) -> None:
    memory = Memory()

    for statement in statements:
        evaluate_statement(memory, statement)


def evaluate_statement(memory: Memory, statement: Statement) -> Value:
    match statement:
        case IntegerToken(value=value):
            return value
        case SymbolToken(value=symbol):
            return evaluate_symbol(memory, symbol)
        case SyntaxTree(items=items):
            evaluated_items = [evaluate_statement(memory, s) for s in items]
            function = evaluated_items.pop(0)

            if not callable(function):
                raise Exception(f"Expected callable, got {function}")

            return function(*evaluated_items)

    raise ValueError(f"Unexpected statement {statement}")


def evaluate_symbol(memory: Memory, symbol: str) -> Value:
    functions = {
        "-": substract,
        "sys-call": partial(evaluate_sys_call, memory),
        "push": partial(evaluate_push, memory),
        "pop": partial(evaluate_pop, memory),
        "~stack-pointer": memory.stack_pointer,
    }

    if symbol in functions:
        return functions[symbol]

    raise Exception(f"unknown symbol {symbol}")


def substract(left: int, right: int) -> int:
    return left - right


def evaluate_push(memory: Memory, value: Value) -> None:
    memory.push_stack(value)


def evaluate_pop(memory: Memory) -> Value:
    return memory.pop_stack()


def evaluate_sys_call(memory: Memory, eax, ebx, ecx = None, edx = None) -> None:
    match eax:
        case 1: # sys_exit
            exit(ebx)
        case 4: # sys_write
            if ebx == 1: # stdout
                print("".join([chr(memory.access(i)) for i in range(ecx, ecx + edx)]))
            else:
                raise NotImplementedError("syscall - unknown file descriptor {ebx}")
        case _:
            raise NotImplementedError(f"syscall - unknown syscall {eax}")
