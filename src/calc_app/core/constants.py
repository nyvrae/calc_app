from collections import namedtuple

Token = namedtuple('Token', ['value', 'type', 'precedence', 'associativity'])

OPERATOR_PRECEDENCE = {
    '+': 2,
    '-': 2,
    '*': 3,
    '/': 3,
    '^': 4,
}