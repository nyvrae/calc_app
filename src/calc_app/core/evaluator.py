from typing import List

from .constants import Token
import math 

class Evaluator:
    """
    A class to evaluate Reverse Polish Notation (RPN) expressions

    Methods:
        evaluate(tokens: List[Token]) -> float:
            Evaluates a list of tokens in RPN and returns the result.   
    """

    _operations = {
        "+": lambda y, x: y + x,
        "-": lambda y, x: y - x,
        "*": lambda y, x: y * x,
        "/": lambda y, x: y / x if x != 0 else (_ for _ in ()).throw(ZeroDivisionError("Error: division by zero")),
        "^": lambda y, x: y ** x
    }
    _functions = {
        "sin": lambda x: math.sin(x),
        "cos": lambda x: math.cos(x),
        "tan": lambda x: math.tan(x),
        "sqrt": lambda x: math.sqrt(x),
        "log": lambda x: math.log(x),
        "ln": lambda x: math.log(x, math.e),
        "abs": lambda x: abs(x),                      
        "exp": lambda x: math.exp(x),                 
        "asin": lambda x: math.asin(x),            
        "acos": lambda x: math.acos(x),                
        "atan": lambda x: math.atan(x),
        "to_degrees": lambda x: math.degrees(x),
        "to_radians": lambda x: math.radians(x),
        "fact": lambda x: math.factorial(int(x)),
    }
    
    def evaluate(self, tokens: List[Token]) -> float:        
        stack = []

        for token in tokens:
            if token.type == "NUMBER":
                stack.append(token.value)
            elif token.value in self._functions:
                x = stack.pop()
                
                stack.append(self._functions[token.value](x))
            elif token.value in self._operations:
                x = stack.pop()
                y = stack.pop()
                
                stack.append(self._operations[token.value](y, x))

        return stack[0]