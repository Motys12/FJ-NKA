# 🤖 Generátor nedeterministických konečnostavových automatov (NKA)

A university project for the **Formálne jazyky** course at TUKE FEI. Implements a generator of **non-deterministic finite automata (NFA)** from regular expressions using top-down recursive descent parsing.

## How It Works

1. **Input** — a regular expression string in standard notation
2. **Lexer** — tokenizes the input string into symbols and operators
3. **Parser** — builds a syntax tree using recursive descent
4. **NKA Generator** — constructs an NFA from the syntax tree
5. **Output** — visual representation of the syntax tree + NFA that accepts the language

## Supported Operations

| Notation | Meaning | Example |
|----------|---------|---------|
| `ab` | Sequence | `ab` matches only "ab" |
| `a\|b` | Alternative | `a\|b` matches "a" or "b" |
| `{R}` | Positive closure (1+) | `{ab}` matches "ab", "abab", ... |
| `[R]` | Optional (0 or 1) | `[a]` matches "" or "a" |

## Example

Input: `{ab|c}`

Syntax tree:
```
regular
└── alternative
    └── sequence
        ├── element <LCBRA>
        ├── regular
        │   ├── sequence: a, b
        │   └── PIPE
        │   └── sequence: c
        └── element <RCBRA>
```

Accepted strings: `ab`, `c`, `abc`, `ababc`, `` (empty string)  
Rejected strings: `a`, `b`, `ac`

## Project Structure

```
ps6/
├── lexer.py        # Lexical analyser — tokenizes input string
├── parser.py       # Recursive descent parser — builds syntax tree
├── nka.py          # NFA generator from syntax tree
├── main.py         # Entry point — reads input, runs pipeline, shows tree
└── requirements.txt
```

## Architecture

```
Input string
     │
     ▼
  [ Lexer ]  ──► tokens
     │
     ▼
  [ Parser ]  ──► syntax tree (anytree)
     │
     ▼
  [ NKA Generator ]  ──► NFA states & transitions
     │
     ▼
  Visual tree + NFA simulation
```

## Installation & Usage

```bash
# Install dependencies
pip install anytree

# Run
python main.py
```

Enter a regular expression when prompted:
```
Enter regular expression: {ab|c}
```

## Implementation Notes

- **Epsilon transitions** — correctly implemented for repetition `{}` using a boolean flag `has_LCBRA` that triggers an epsilon back-transition to the start state
- **Modular design** — each component (Lexer, Parser, NKA) is independently testable
- **anytree** library used for syntax tree visualization

## Author

**Dmytro Shkyl**  
TUKE — Faculty of Electrical Engineering and Informatics  
Formálne jazyky, 2024/2025
