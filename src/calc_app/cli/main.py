from ..core.parser import Parser
from ..core.evaluator import Evaluator

def main():
    try:
        user_input = input()
        if not user_input:
            raise ValueError("Please enter an expression")
        
        parser = Parser()
        evaluator = Evaluator()

        tokens = parser.parse(user_input)
        if not tokens:
            raise ValueError("Invalid expression")
        
        print("Tokens:", [token for token in tokens])
        
        result = evaluator.evaluate(tokens)
        
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()