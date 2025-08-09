from ..core.parser import Parser
from ..core.calculator import Calculator

def main():
    user_input = input()
    
    parser = Parser()
    tokens = parser.parse(user_input)    
    
    # print(tokens)
    
    calculator = Calculator()
    
    result = calculator.calculate(tokens)
    
    # print(result)

if __name__ == "__main__":
    main()