from enum import Enum, auto

class TokenType(Enum):
    SYMBOL = auto()    
    
    PIPE = auto()        # '|'
    LBRACKET = auto()    # '['
    RBRACKET = auto()    # ']'
    LPAREN = auto()      # '('
    RPAREN = auto()      # ')'
    LBRACE = auto()      # '{'
    RBRACE = auto()      # '}'
    EOF = auto()         # 'End Of File'

class Token:
    def __init__(self, type, value=None):
        self.type = type 
        self.attribute = value  

    def __repr__(self): #string representation token
        if self.attribute is not None:
            return f"Token({self.type}, {self.attribute})"
        return f"Token({self.type})"
    

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text   
        self.pos = 0    
        self.current_char = self.input_text[0] if input_text else None 
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.input_text):
            self.current_char = self.input_text[self.pos]
        else:
            self.current_char = None 
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalnum(): #isalpha() and isdigit()
                symbol = self.current_char
                self.advance()
                return Token(TokenType.SYMBOL, symbol)

            if self.current_char == '|':
                self.advance()
                return Token(TokenType.PIPE)
            
            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET)
            
            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)
            
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE)
            
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE)
            
            raise ValueError(f"Nerozpoznaný znak: '{self.current_char}'")
        
        # Keď prejdeme celý text, vrátime token konca vstupu
        return Token(TokenType.EOF)