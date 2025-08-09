import re
from collections import namedtuple
from typing import Optional

Token = namedtuple('Token', ['value', 'type', 'precedence'])

OPERATOR_PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}

class Parser:
    def __init__(self):
        self._pattern = re.compile(r"(\d+\.?\d*)|([+\-*/])")

    def parse(self, expression: str) -> list[Token]:
        if not expression:
            return []
        
        expression = expression.replace(' ', '')  
        
        tokens_raw = re.findall(self._pattern, expression)
        
        tokens = []

        for number, operator in tokens_raw:
            if number:
                tokens.append(Token(value=float(number), type='NUMBER', precedence=None))
            elif operator:
                tokens.append(Token(value=operator, type='OPERATOR', precedence=OPERATOR_PRECEDENCE[operator]))
        
        return tokens