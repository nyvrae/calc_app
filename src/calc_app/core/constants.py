from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Token:
    value: float | str
    type: str
    precedence: Optional[int] = None
    associativity: Optional[str] = None

OPERATOR_PRECEDENCE = {
    '+': 2,
    '-': 2,
    '*': 3,
    '/': 3,
    '^': 4,
    "u-": 5,
    "u+":  5
}