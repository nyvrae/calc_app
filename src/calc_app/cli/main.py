from ..core.parser import Parser
from ..core.evaluator import Evaluator

def main():
    user_input = input()
    
    parser = Parser()
    evaluator = Evaluator()

    tokens = parser.parse(user_input)    
    
    print([token.value for token in tokens])
    
    result = evaluator.evaluate(tokens)
    
    print(result)

if __name__ == "__main__":
    main()