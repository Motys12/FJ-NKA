from LexerFJ import TokenType
from anytree import Node, RenderTree

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer                        
        self.current_token = self.lexer.get_next_token()  
    
    def consume(self, expected_token_type):
        if self.current_token.type == expected_token_type:
            self.current_token = self.lexer.get_next_token()  
        else:
            raise SyntaxError(f"Syntaktická chyba: očakávaný token {expected_token_type}, " 
                             f"získaný {self.current_token.type}")
    

    def Alternative(self):
        left = self.Sequence()  

        if self.current_token.type == TokenType.PIPE:
            nodes = [left]  
            while self.current_token.type == TokenType.PIPE:
                self.consume(TokenType.PIPE) 
                nodes.append(self.Sequence())  
            if len(nodes) > 1:
                node = nodes[0]
                for next_node in nodes[1:]:
                    node = ("alternative", node, next_node)
                return node
            return nodes[0]
        else:
            return left
        
    
    def Sequence(self):
        nodes = []
        while self.current_token.type not in {TokenType.PIPE, TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE, TokenType.EOF}:
            nodes.append(self.Factor())

        return ("sequence", nodes)
 
        
    def Factor(self):
        token = self.current_token
        
        if token.type == TokenType.SYMBOL:
            self.consume(TokenType.SYMBOL)
            return ("element", ("SYMBOL", token.attribute))

        if token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)  
            result = ("regular", self.Alternative()) 
            self.consume(TokenType.RPAREN) 
            return ("element",result)
        
        if token.type == TokenType.LBRACE: 
            self.consume(TokenType.LBRACE)
            expr = ("regular", self.Alternative())
            self.consume(TokenType.RBRACE)
            return ("element", ("LCBRA", expr, "RCBRA"))

        if token.type == TokenType.LBRACKET:  
            self.consume(TokenType.LBRACKET)
            expr = ("regular", self.Factor())
            self.consume(TokenType.RBRACKET)
            return ("element", ("LBRCKT", expr, "RBRCKT"))

        else:
            raise SyntaxError(f"Neočakávaný token: {token}")
        
def visualize_tree(parsed_tree):
    def has_pipe(node, depth=0):
        indent = "  " * depth
        if isinstance(node, tuple):
            if node[0] == "alternative":
                return True
            for child in node[1:]:
                if has_pipe(child, depth + 1):
                    return True
        elif isinstance(node, list):
            for child in node:
                if has_pipe(child, depth + 1):
                    return True
        return False

    
     
    def build_tree(node, parent=None):
        if isinstance(node, tuple):
            label = node[0]
            new_node = Node(label, parent=parent)
        
            if label == "element":
                content = node[1]
                if isinstance(content, tuple) and content[0] == "LCBRA":
                    Node("<LCBRA>", parent=new_node)
                    build_tree(content[1], new_node)
                    Node("<RCBRA>", parent=new_node)
                elif isinstance(content, tuple) and content[0] == "LBRCKT":
                    Node("<LBRCKT>", parent=new_node)
                    build_tree(content[1], new_node)
                    Node("<RBRCKT>", parent=new_node)
                else:
                    build_tree(content, new_node)
            elif label == "regular": 
                build_tree(node[1], new_node)
            elif label == "alternative":
                build_tree(node[1], new_node)
                Node("PIPE", parent=new_node)
                build_tree(node[2], new_node)
            elif label == "sequence":
                for child in node[1]:
                    build_tree(child, new_node)    
            else:
                for child in node[1:]:
                    build_tree(child, new_node)
        else:
            Node(str(node), parent=parent)

    root = Node("regular")
    if has_pipe(parsed_tree):
        alt_node = Node("alternative", parent=root)
        build_tree(parsed_tree, parent=alt_node)
    else:
        build_tree(parsed_tree, parent=root)

    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")
