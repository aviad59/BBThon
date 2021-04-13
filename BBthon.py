
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
        res += f':{self.pos_start.line + 1} הרוש {self.pos_start.file_name} :ץבוקב הז\n'
        res += f'{self.details}'
        return res

class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end): 
        super().__init__("...הפ תבתכ המ גשומ יל ןיא ?חא עמוש", details, pos_start, pos_end)

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

    def forward(self, curChar):
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

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

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
                tokens.append(Token(T_PLUS))
                self.forward()
            elif self.curChar == '-':
                tokens.append(Token(T_MINUS))
                self.forward()
            elif self.curChar == '*':
                tokens.append(Token(T_MUL))
                self.forward()
            elif self.curChar == '/':
                tokens.append(Token(T_DIV))
                self.forward() 
            elif self.curChar == '(':
                tokens.append(Token(T_LPAREN))
                self.forward() 
            elif self.curChar == ')':
                tokens.append(Token(T_RPAREN))
                self.forward() 
            else:
                pos_start = self.pos.copy()
                char = self.curChar
                self.forward()
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos)

        return tokens, None

    def create_number(self):
        num_str = ' '
        dot_count = 0

        while self.curChar != None and self.curChar in DIGITS + '.':
            if self.curChar == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else: 
                num_str += self.curChar
            self.forward()
            
        if dot_count == 0:
            return Token(T_INT, int(num_str))
        else:
            return Token(T_FLOAT, float(num_str))
########################
# Run
########################
def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.create_tokens()

    return tokens, error
