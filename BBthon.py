
######################
# Constants
######################

DIGITS = '1234567890'

######################
# Errors
######################

class Error:
    def __init__(self, title, details, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_title = title
        self.details = details

    def __repr__(self):
        res = f'{self.error_title}\n'
        res += f':{self.pos_start.line + 1} הרושב {self.pos_start.file_name} :ץבוקב הז\n'
        res += f'{self.details}'
        return res

class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end): 
        super().__init__(" ינלאמש הזה ותה ,םירקי םיחרזא", details, pos_start, pos_end)

class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__("הזה חוסינה תא ןיבמ אל ינא יכ ,רפסה תיבל רוזחתש ידכ דיפל", details, pos_start, pos_end)

#######################
# Nodes
######################

class NumberNode:
    def __init__(self, tok):
        self.token = tok

    def __repr__(self):
        return f'{self.token}'

class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.lNode = left_node
        self.op_token = op_token
        self.rNode = right_node
    
    def __repr__(self):
        return f'({self.lNode}, {self.op_token}, {self.rNode})'

class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token}, {self.node})'

####################
# Parser
####################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_index = -1
        self.forward()

    def forward(self):
        self.tok_index += 1
        if self.tok_index < len(self.tokens):
            self.cur_token = self.tokens[self.tok_index]
        return self.cur_token

    def parse(self):
        res = self.expression()
        if not res.error and self.cur_token.type != T_EOF:
            return res.failure(InvalidSyntaxError("- + / * ) ( :ב שמתשת השקבב תיטמתמ הלועפ אל תאז", self.cur_token.pos_start, self.cur_token.pos_end))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.cur_token

        if tok.type in (T_PLUS, T_MINUS):
            res.register(self.forward())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        elif tok.type in (T_INT, T_FLOAT):
            res.register(self.forward())
            return res.success(NumberNode(tok))
        
        elif tok.type == T_LPAREN:
            res.register(self.forward())
            expr = res.register(self.expression())
            if res.error: return res
            if self.cur_token.type == T_RPAREN:
                res.register(self.forward())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError("תרגס אלו קית ילע תחתפ", self.cur_token.pos_start, self.cur_token.pos_end))

        return res.failure(InvalidSyntaxError("רפסמל יתיפיצ", tok.pos_start, tok.pos_end))

    def term(self):
        return self.extract_op(self.factor, (T_MUL, T_DIV))
    
    def expression(self):
        return self.extract_op(self.term, (T_PLUS, T_MINUS))

    def extract_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        
        if res.error: return res

        while self.cur_token.type in ops:
            op_tok = self.cur_token
            res.register(self.forward())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

######################
# Parse Result
#####################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        
        return res
        
    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
        

######################
# Position
#####################

class Position:
    def __init__(self, index, line, column, file_name, file_text):
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_text = file_text

    def forward(self, curChar=None):
        self.index += 1
        self.column += 1

        if curChar == '\n':
            self.line += 1
            self.column = 0
        
        return self
    
    def copy(self):
        return Position(self.index, self.line, self.column, self.file_name, self.file_text)

######################
# Tokens
######################

T_INT = "T_INT"
T_FLOAT = "FLOAT"

T_PLUS = "PLUS"
T_MINUS = "MINUS"
T_MUL = "MUL"
T_DIV = "DIV"

T_LPAREN = "LPAREN"
T_RPAREN = "RPAREN"

T_EOF = "EOF"

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start
            self.pos_end = pos_start.copy()
            self.pos_end.forward()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

######################
# Lexer
######################
class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.curChar = None
        self.forward()
    
    def forward(self):
        self.pos.forward(self.curChar)
        self.curChar = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def create_tokens(self):
        tokens = []

        while self.curChar != None:
            if self.curChar in ' \t':
                self.forward()
            elif self.curChar in DIGITS:
                tokens.append(self.create_number())

            elif self.curChar == '+':
                tokens.append(Token(T_PLUS, pos_start=self.pos))
                self.forward()
            elif self.curChar == '-':
                tokens.append(Token(T_MINUS, pos_start=self.pos))
                self.forward()
            elif self.curChar == '*':
                tokens.append(Token(T_MUL, pos_start=self.pos))
                self.forward()
            elif self.curChar == '/':
                tokens.append(Token(T_DIV, pos_start=self.pos))
                self.forward() 
            elif self.curChar == '(':
                tokens.append(Token(T_LPAREN, pos_start=self.pos))
                self.forward() 
            elif self.curChar == ')':
                tokens.append(Token(T_RPAREN, pos_start=self.pos))
                self.forward() 
            else:
                pos_start = self.pos.copy()
                char = self.curChar
                self.forward()
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos)

        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens, None

    def create_number(self):
        num_str = ' '
        dot_count = 0
        pos_start = self.pos.copy()

        while self.curChar != None and self.curChar in DIGITS + '.':
            if self.curChar == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else: 
                num_str += self.curChar
            self.forward()
            
        if dot_count == 0:
            return Token(T_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(T_FLOAT, float(num_str), pos_start, self.pos)

########################
# Run
########################
def run(file_name, text):

    lexer = Lexer(file_name, text)
    tokens, error = lexer.create_tokens()

    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
