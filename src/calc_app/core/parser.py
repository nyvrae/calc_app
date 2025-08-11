import re
from .constants import Token, OPERATOR_PRECEDENCE

from typing import List

class Parser:
    def __init__(self):
        self._pattern = re.compile(r"(\d+\.?\d*)|([+\-*/])|(\^)|([()])")
        
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
                if operator_stack and operator_stack[-1].type == "LPAREN":
                    operator_stack.pop()

        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue


    def parse(self, expression: str) -> list[Token]:
        if not expression:
            return []
        
        expression = expression.replace(' ', '')  
        
        tokens_raw = re.findall(self._pattern, expression)
        
        tokens = []

        for number, left_op, right_op, paren in tokens_raw:
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
        
        return self._to_rpn(tokens)