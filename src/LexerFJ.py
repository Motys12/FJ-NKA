from enum import Enum, auto

class TokenType(Enum):
    SYMBOL = auto()    
    
    # SEQUENCE = auto()    # R1R2
    # ALTERNATIVE = auto() # R1|R2
    # TRANSITIVE = auto()  # {R} 
    # POSITIVE = auto()    # R{R}
    # OPTIONAL = auto()    # [R]
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

    def __repr__(self):
        if self.attribute is not None:
            return f"Token({self.type}, {self.attribute})"
        return f"Token({self.type})"
    

# Lexikálny analyzátor - rozpoznáva a extrahuje tokeny zo vstupného reťazca
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text   
        self.pos = 0    
        self.current_char = self.input_text[0] if input_text else None 
    
    def advance(self):
        """Posunie pozíciu na ďalší znak a aktualizuje current_char.
        Ak sa dostane za koniec textu, nastaví current_char na None."""
        self.pos += 1
        if self.pos < len(self.input_text):
            self.current_char = self.input_text[self.pos]
        else:
            self.current_char = None 
    
    def skip_whitespace(self):
        """Preskočí všetky medzery a nové riadky vo vstupe."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def get_next_token(self):
        """Hlavná metóda lexikálneho analyzátora.
        Analyzuje text a vracia ďalší token v poradí."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
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