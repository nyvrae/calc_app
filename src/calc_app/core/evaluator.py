from typing import List

from .constants import Token

class Evaluator:
    _operations = {
        "+": lambda y, x: y + x,
        "-": lambda y, x: y - x,
        "*": lambda y, x: y * x,
        "/": lambda y, x: y / x if x != 0 else (_ for _ in ()).throw(ZeroDivisionError("Error: division by zero")),
        "^": lambda y, x: y ** x
    }
    
    def evaluate(self, tokens: List[Token]) -> float:
        stack = []

        for token in tokens:
            if token.type == "NUMBER":
                stack.append(token.value)
            elif token.value in self._operations:
                x = stack.pop()
                y = stack.pop()
                
                stack.append(self._operations[token.value](y, x))

        return stack[0]