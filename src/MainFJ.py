from LexerFJ import Lexer
from ParserFJ import Parser, visualize_tree
from NkaFJ import regex_to_nka

if __name__ == "__main__":
    print("Enter regular (enter 'quit' for exit):")
    running = True 

    while running:
        input_text = input("> ")

        if input_text.lower() == "quit":
            print("!...Exiting...!")
            running = False  
            break  

        if input_text.strip() == "":
            continue

        lexer = Lexer(input_text)
        parser = Parser(lexer)

        try:
            parsed_tree = parser.Alternative()
            visualize_tree(parsed_tree)
            nka = regex_to_nka(parsed_tree)

            while True:
                try:
                    test_string = input("Enter string to test acceptation(or 'quit' to exit): ")
                    if test_string.lower() == "quit":
                        print("Exit.....")
                        running = False  
                        break 
                    if " " in test_string:
                        print("Error: The string contains spaces. Please enter a valid string without spaces.")
                        continue
                    if nka.is_accepted(test_string):
                        print(f"String '{test_string}' is ACCEPTED!")
                    else:
                        print(f"String '{test_string}' is NOT ACCEPTED!")
                except KeyboardInterrupt:
                    print("\n!...Exiting...!")
                    running = False  
                    break  
        except SyntaxError as e:
            print(f"Error: {e}")