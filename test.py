def shunting_yard(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output_queue = []
    operator_stack = []

    tokens = expression.split()

    for token in tokens:
        if token.isdigit():
            output_queue.append(token)
        elif token in precedence:
            while (operator_stack and operator_stack[-1] in precedence and
                    precedence[operator_stack[-1]] >= precedence[token]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue

def evaluate_rpn(tokens):
    stack = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
    return stack[0]

expr = "1 + 2 * 6 - 7"
rpn = shunting_yard(expr)
print("RPN:", rpn)
print("Result:", evaluate_rpn(rpn))

