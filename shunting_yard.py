#!/usr/bin/env python3
import sys
import operator
from typing import Generator

op_funcs = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
}


def eval_op(op: str, op1: int, op2: int) -> int:
    return op_funcs[op](op1, op2)


def precedence(op: str) -> int:
    if op == "^":
        return 4
    elif op in "*/":
        return 3
    elif op in "+-":
        return 2
    else:
        return 0


def associativity(op: str) -> str:
    if op in "*/-+":
        return "left"
    else:
        return "right"


def tokenize(expr: str) -> Generator[str, None, None]:
    number: str = ""
    end: int = len(expr) - 1
    for i, char in enumerate(expr):
        if char.isspace():
            continue

        if char.isdigit():
            if number and number[0].isdigit():
                number += char
            else:
                number = char

        if number and (i == end or not char.isdigit()):
            yield number
            number = ""

        if char in "+-*/^()":
            yield char


def shunting_yard(expr: str) -> list[str]:
    op_stack: list[str] = []
    output: list[str] = []
    for token in tokenize(expr):
        if not token:
            continue
        if token.isdigit():
            output.append(token)
        elif token in "+-*/^":
            if op_stack:
                while op_stack and (
                    (
                        op_stack[-1] != "("
                        and precedence(op_stack[-1]) > precedence(token)
                    )
                    or (
                        precedence(op_stack[-1]) == precedence(token)
                        and associativity(token) == "left"
                    )
                ):
                    output.append(op_stack.pop())
            op_stack.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            if op_stack:
                while op_stack[-1] != "(":
                    output.append(op_stack.pop())
            if op_stack[-1] == "(":
                op_stack.pop()

    while op_stack:
        if op_stack[-1] != "(":
            output.append(op_stack.pop())

    return output


def evaluate_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in "+-*/^":
            op2 = stack.pop()
            op1 = stack.pop()
            stack.append(eval_op(token, op1, op2))
    return stack[0]


def main(expr: str) -> None:
    tokens: list[str] = shunting_yard(expr)
    print(evaluate_rpn(tokens))


if __name__ == "__main__":
    main(sys.argv[1])
