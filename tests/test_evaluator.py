import pytest
from calc_app.core.evaluator import Evaluator, Token
import math

@pytest.fixture
def evaluator():
    return Evaluator()

@pytest.mark.parametrize(
    "tokens, expected_result",
    [
        ([Token(3.0, "NUMBER"),
          Token(4.0, "NUMBER"),
          Token("+", "OPERATOR")], 7.0),

        ([Token(3.0, "NUMBER"),
          Token(4.0, "NUMBER"),
          Token(5.0, "NUMBER"),
          Token("+", "OPERATOR"),
          Token("*", "OPERATOR")], 27),

        ([Token(2.0, "NUMBER"),
          Token(3.0, "NUMBER"),
          Token("^", "OPERATOR")], 8.0)
    ]
)
def test_basic_arithmetic(evaluator, tokens, expected_result):
    assert evaluator.evaluate(tokens) == expected_result

def test_unary_operators(evaluator):
    tokens_uminus = [
        Token(5.0, "NUMBER"),
        Token("uminus", "FUNCTION")
    ]
    assert evaluator.evaluate(tokens_uminus) == -5.0

    tokens_uplus = [
        Token(5.0, "NUMBER"),
        Token("uplus", "FUNCTION")
    ]
    assert evaluator.evaluate(tokens_uplus) == 5.0

@pytest.mark.parametrize(
    "tokens, expected_result, not_more_than",
    [
        ([Token(math.pi, "NUMBER"),
          Token(2.0, "NUMBER"),
          Token("/", "OPERATOR"),
          Token("sin", "FUNCTION")], 1.0, 1e-10),

        ([Token(math.e, "NUMBER"),
          Token("ln", "FUNCTION")], 1.0, 1e-10)
    ]
)
def test_mathematical_functions(evaluator, tokens, expected_result, not_more_than):
    assert abs(evaluator.evaluate(tokens) - expected_result) < not_more_than

def test_factorial(evaluator):
    tokens = [
        Token(5.0, "NUMBER"),
        Token("fact", "FUNCTION")
    ]
    assert evaluator.evaluate(tokens) == 120.0

def test_trigonometric_conversions(evaluator):
    tokens_to_degrees = [
        Token(math.pi, "NUMBER"),
        Token("to_degrees", "FUNCTION")
    ]
    assert abs(evaluator.evaluate(tokens_to_degrees) - 180.0) < 1e-10

    tokens_to_radians = [
        Token(180.0, "NUMBER"),
        Token("to_radians", "FUNCTION")
    ]
    assert abs(evaluator.evaluate(tokens_to_radians) - math.pi) < 1e-10

def test_complex_expression(evaluator):
    tokens = [
        Token(2.0, "NUMBER"),
        Token(3.0, "NUMBER"),
        Token(4.0, "NUMBER"),
        Token("+", "OPERATOR"),
        Token(2.0, "NUMBER"),
        Token("^", "OPERATOR"),
        Token("*", "OPERATOR"),
        Token(7.0, "NUMBER"),
        Token("/", "OPERATOR")
    ]
    assert abs(evaluator.evaluate(tokens) - (2 * (3 + 4) ** 2 / 7)) < 1e-10

def test_error_handling(evaluator):
    tokens_div_by_zero = [
        Token(5.0, "NUMBER"),
        Token(0.0, "NUMBER"),
        Token("/", "OPERATOR")
    ]
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        evaluator.evaluate(tokens_div_by_zero)

    with pytest.raises(ValueError, match="Invalid expression"):
        evaluator.evaluate([])