import pytest
from calc_app.core.parser import Parser, Token

@pytest.fixture
def parser():
    return Parser()

@pytest.mark.parametrize(
    "expression, expected_len",
    [
        ("1 + 2", 3),
        ("1 - 7", 3),
        ("8 * 3", 3),
        ("8 / 2", 3),
        ("2 ^ 3", 3),
        ("2 + 3 * 4", 5),
        ("2 * 3 + 4", 5),
        ("2 + 3 ^ 2 * 4", 7),
        ("  10   +  5 ", 3),
        ("100/  10", 3),
    ]
)
def test_basic_operations(parser, expression, expected_len):
    tokens = parser.parse(expression)
    assert len(tokens) == expected_len

@pytest.mark.parametrize(
    "expression, expected_len",
    [
        ("2 * (3 + 4)", 5),
        ("1 + (2 * (3 + 4))", 7),
        ("(1 + 2) * (3 + 4)", 7),
    ]
)
def test_parentheses(parser, expression, expected_len):
    tokens = parser.parse(expression)
    assert len(tokens) == expected_len

@pytest.mark.parametrize(
    "expression, expected_values",
    [
        ("pi + e", [Token(type='NUMBER', value=3.141592653589793, precedence=None, associativity=None),
                    Token(type='NUMBER', value=2.718281828459045, precedence=None, associativity=None)]),
    ]
)
def test_constants(parser, expression, expected_values):
    tokens = parser.parse(expression)
    values_in_tokens = [t.value for t in tokens if t.type == "NUMBER"]
    for val in expected_values:
        assert val.value in values_in_tokens

@pytest.mark.parametrize(
    "expression, function_name",
    [
        ("sin(0)", "sin"),
        ("cos(pi)", "cos"),
        ("tan(1)", "tan"),
        ("sqrt(4)", "sqrt"),
        ("log(10)", "log"),
        ("ln(e)", "ln"),
        ("abs(-5)", "abs"),
        ("exp(2)", "exp"),
        ("asin(1)", "asin"),
        ("acos(0)", "acos"),
        ("atan(1)", "atan"),
        ("to_degrees(3.141592653589793)", "to_degrees"),
        ("to_radians(180)", "to_radians"),
        ("fact(5)", "fact"),
    ]
)
def test_functions(parser, expression, function_name):
    tokens = parser.parse(expression)
    assert any(t.type == "FUNCTION" and t.value == function_name for t in tokens)

def test_nested_functions(parser):
    expr = "sin(sin(10))"
    tokens = parser.parse(expr)
    function_count = sum(1 for t in tokens if t.type == "FUNCTION")
    assert function_count == 2

@pytest.mark.parametrize(
    "expression",
    [
        "1.5 + 2.7",
        "3.14 * 2.0",
        "0.5 / 0.25"
    ]
)
def test_float_numbers(parser, expression):
    tokens = parser.parse(expression)
    assert all(isinstance(t.value, float) for t in tokens if t.type == "NUMBER")

def test_mixed_expression(parser):
    expr = "sin(pi / 2) + log(10) - sqrt(4)"
    tokens = parser.parse(expr)
    function_names = [t.value for t in tokens if t.type == "FUNCTION"]
    for func in ["sin", "log", "sqrt"]:
        assert func in function_names
    assert any(t.type == "NUMBER" for t in tokens)

@pytest.mark.parametrize(
    "expression, expected_tokens",
    [
        ("-5", [Token(value=5.0, type='NUMBER'), Token(value='u-', type='FUNCTION')]),
        ("+10", [Token(value=10.0, type='NUMBER'), Token(value='u+', type='FUNCTION')]),
        ("2 * (-3)", [
            Token(value=2.0, type='NUMBER'),
            Token(value=3.0, type='NUMBER'),
            Token(value='u-', type='FUNCTION'),
            Token(value='*', type='OPERATOR')
        ]),
        ("5 + (+2)", [
            Token(value=5.0, type='NUMBER'),
            Token(value=2.0, type='NUMBER'),
            Token(value='u+', type='FUNCTION'),
            Token(value='+', type='OPERATOR'),
        ]),
    ]
)
def test_unary_operators(parser, expression, expected_tokens):
    tokens = parser.parse(expression)
    for actual, expected in zip(tokens, expected_tokens):
        assert actual.type == expected.type
        assert actual.value == expected.value

def test_complex_expression(parser):
    expr = "3 + 5 * (6 + 10 - sin(5))"
    tokens = parser.parse(expr)
    assert len(tokens) > 5
    assert any(t.type == "FUNCTION" for t in tokens)

# @pytest.mark.parametrize(
#     "expression",
#     [
#         "1 + ",
#         "(1 + 2",
#         "3 + * 4",
#     ]
# )
# def test_invalid_expressions(parser, expression):
#     with pytest.raises(Exception):
#         parser.parse(expression)