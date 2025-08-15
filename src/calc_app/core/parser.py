import re
from .constants import Token, OPERATOR_PRECEDENCE

from typing import List
import math

class Parser:
    """
    A class to parse arithmetic expressions and convert them into 
    Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

    Methods:
        _tokenize(expression: str) -> List[Token]:
            Internal method that splits an expression string into 
            individual tokens and returns a list of tokens.

        _to_rpn(tokens: List[Token]) -> List[Token]:
            Internal method that applies the Shunting Yard algorithm 
            to a list of tokens and returns the RPN output queue.

        parse(expression: str) -> List[Token]:
            Parses an infix expression string and returns a list of tokens 
            in RPN order.
    """

    def __init__(self):
        self._pattern = re.compile(r"(\d+\.?\d*)|([+\-*/])|(\^)|([()])|(sin|cos|tan|sqrt|log|ln|abs|exp|asin|acos|atan|to_degrees|to_radians|fact)|(pi|e)")

    def _tokenize(self, expression: str) -> List[Token]:
        tokens = []
        tokens_raw = re.findall(self._pattern, expression)

        for number, op, power, paren, func, constant in tokens_raw:
            is_unary = op and op in "+-" and (not tokens or tokens[-1].type in ["OPERATOR", "LPAREN"])

            if number:
                tokens.append(Token(float(number), "NUMBER"))
            elif is_unary:
                tokens.append(Token(f"u{op}", "FUNCTION"))
            elif op:
                tokens.append(Token(op, "OPERATOR", OPERATOR_PRECEDENCE[op], "left"))
            elif power:
                tokens.append(Token(power, "OPERATOR", OPERATOR_PRECEDENCE[power], "right"))
            elif paren:
                tokens.append(Token(paren, "LPAREN" if paren == "(" else "RPAREN"))
            elif constant:
                value = math.pi if constant == "pi" else math.e
                tokens.append(Token(value, "NUMBER"))
            elif func:
                tokens.append(Token(func, "FUNCTION"))
        return tokens

    def _to_rpn(self, tokens: List[Token]) -> List[Token]:    
        output = []
        op_stack = []
        
        for token in tokens:
            if token.type == "NUMBER":
                output.append(token)
            elif token.type == "FUNCTION":
                op_stack.append(token)
            elif token.type == "OPERATOR":
                while op_stack and (op_stack[-1].type != "LPAREN") and (
                OPERATOR_PRECEDENCE.get(op_stack[-1].value) > OPERATOR_PRECEDENCE.get(token.value, 0)
                or (
                    token.associativity == "left" and 
                    OPERATOR_PRECEDENCE.get(op_stack[-1].value) == OPERATOR_PRECEDENCE.get(token.value, 0)
                    )
                ):
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token.type == "LPAREN":
                op_stack.append(token)
            elif token.type == "RPAREN":
                while op_stack and op_stack[-1].type != "LPAREN":
                    output.append(op_stack.pop())
                if op_stack:
                    op_stack.pop()
                if op_stack and op_stack[-1].type == "FUNCTION":
                    output.append(op_stack.pop())

        while op_stack:
            output.append(op_stack.pop())
        
        return output

    def parse(self, expression: str) -> list[Token]:
        if not expression:
            return []
        
        expression = expression.replace(' ', '')
        tokens = self._tokenize(expression)
        return self._to_rpn(tokens)