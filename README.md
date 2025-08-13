# Calculator App

A command-line calculator application that supports parsing and evaluating arithmetic expressions using the [**Shunting Yard algorithm**](https://en.wikipedia.org/wiki/Shunting_yard_algorithm) and [**Reverse Polish Notation (RPN)** evaluation](https://www.geeksforgeeks.org/dsa/evaluate-the-value-of-an-arithmetic-expression-in-reverse-polish-notation-in-java/).

## ✨ Features

- Supports basic arithmetic operations:

  - Addition (`+`)
  - Subtraction (`-`)
  - Multiplication (`*`)
  - Division (`/`)
  - Exponentiation (`^`)

- Parentheses for grouping operations
- Follows standard operator precedence and associativity rules
- Implements the Shunting Yard algorithm for expression parsing
- Converts infix notation to Reverse Polish Notation (RPN) before evaluation

---

## 🚀 Usage

Run the application from the command line:

```bash
python -m src.calc_app.cli.main
```

Then enter an expression, for example:

```
5 + 4^2 * (24 / 2 - 160)
```

Example output:

```
[5.0, 4.0, 2.0, '^', 24.0, 2.0, '/', 160.0, '-', '*', '+']
Result: -995.0
```

---

## 🗂 Project Structure

```
src/
  calc_app/
    cli/
      main.py        # Entry point for CLI
    core/
      tokenizer.py   # Converts expressions into tokens
      parser.py      # Implements Shunting Yard algorithm
      evaluator.py   # Evaluates RPN expressions
    ...
```

---
