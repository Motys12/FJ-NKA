from LexerFJ import Lexer
from ParserFJ import Parser, visualize_tree


def main():
    print("Введите регулярное выражение (или напишите 'quit' для выхода):")

    while True:
        input_text = input("> ")

        if input_text.lower() == "quit":
            print("Выход из программы.")
            break

        if input_text.strip() == "":
            continue

        lexer = Lexer(input_text)
        parser = Parser(lexer)

        try:
            parsed_tree = parser.Alternative()
            visualize_tree(parsed_tree)
        except SyntaxError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()