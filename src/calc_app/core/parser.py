import re
from .constants import Token, OPERATOR_PRECEDENCE

from typing import List
import math

class Parser:
    """
    A class to parse arithmetic expressions and convert them into 
    Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

    Methods:
        parse(expression: str) -> List[Token]:
            Parses an infix expression string and returns a list of tokens 
            in RPN order.

        _to_rpn(tokens: List[Token]) -> List[Token]:
            Internal method that applies the Shunting Yard algorithm 
            to a list of tokens and returns the RPN output queue.
    """

    def __init__(self):
        self._pattern = re.compile(r"(\d+\.?\d*)|([+\-*/])|(\^)|([()])|(exp)|(pi|e)|([a-zA-Z_][a-zA-Z_]*)")
        
    def _to_rpn(self, tokens: List[Token]) -> List[Token]:    
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if token.type == "NUMBER":
                output_queue.append(token)
            elif token.type == "FUNCTION":
                operator_stack.append(token)
            elif token.type == "OPERATOR":
                while operator_stack and (operator_stack[-1].type != "LPAREN") and (
                OPERATOR_PRECEDENCE[operator_stack[-1].value] > token.precedence
                or (
                    token.associativity == "left" and 
                    OPERATOR_PRECEDENCE[operator_stack[-1].value] == token.precedence)
                ):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == "LPAREN":
                operator_stack.append(token)
            elif token.type == "RPAREN":
                while operator_stack and operator_stack[-1].type != "LPAREN":
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
                if operator_stack and operator_stack[-1].type == "FUNCTION":
                    output_queue.append(operator_stack.pop())

        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue


    def parse(self, expression: str) -> list[Token]:
        if not expression:
            return []
        
        expression = expression.replace(' ', '')  
        
        tokens_raw = re.findall(self._pattern, expression)
        
        tokens = []

        for number, left_op, right_op, paren, exponent, constant, function in tokens_raw:
            if number:
                tokens.append(Token(value=float(number), type='NUMBER', precedence=None, associativity=None))
            elif left_op:
                tokens.append(Token(value=left_op, type='OPERATOR',
                                    precedence=OPERATOR_PRECEDENCE[left_op], associativity="left"))
            elif right_op:
                tokens.append(Token(value=right_op, type='OPERATOR',
                                    precedence=OPERATOR_PRECEDENCE[right_op], associativity="right"))
            elif paren:
                if paren == "(":
                    tokens.append(Token(value=paren, type='LPAREN', precedence=None, associativity=None))
                else:
                    tokens.append(Token(value=paren, type='RPAREN', precedence=None, associativity=None))
                    
            elif constant:
                if constant == "pi":
                    tokens.append(Token(value=math.pi, type="NUMBER", precedence=None, associativity=None))
                elif constant == "e":
                    tokens.append(Token(value=math.e, type="NUMBER", precedence=None, associativity=None))

            elif function or exponent:
                if function:
                    tokens.append(Token(value=function, type="FUNCTION", precedence=None, associativity=None))
                else:
                    tokens.append(Token(value=exponent, type="FUNCTION", precedence=None, associativity=None))
        return self._to_rpn(tokens)