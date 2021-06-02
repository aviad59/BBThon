from Parser import *
from constants import *
from errors import *
from Interpreter import *
  
######################
#      Position      #
######################
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
#       Tokens       #
######################
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.forward()

        if pos_end:
            self.pos_end = pos_end

    def match(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

######################
#       Lexer        #
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
            elif self.curChar in ':\n':
                tokens.append(Token(T_NEWLINE, pos_start=self.pos))
                self.forward()
            elif self.curChar in DIGITS:
                tokens.append(self.create_number())
            elif self.curChar in LETTERS:
                tokens.append(self.create_identifier())
            elif self.curChar == '"':
                tokens.append(self.create_string())
            elif self.curChar == '+':
                tokens.append(Token(T_PLUS, pos_start=self.pos))
                self.forward()
            elif self.curChar == '-':
                tokens.append(self.create_minus_or_arrow())
            elif self.curChar == '*':
                tokens.append(Token(T_MUL, pos_start=self.pos))
                self.forward()
            elif self.curChar == '/':
                tokens.append(Token(T_DIV, pos_start=self.pos))
                self.forward()
            elif self.curChar == "$":
                tokens.append(Token(T_DOLLAR, pos_start=self.pos))
                self.forward()
            elif self.curChar == '^':
                tokens.append(Token(T_POW, pos_start=self.pos))
                self.forward() 
            elif self.curChar == '(':
                tokens.append(Token(T_LPAREN, pos_start=self.pos))
                self.forward() 
            elif self.curChar == ')':
                tokens.append(Token(T_RPAREN, pos_start=self.pos))
                self.forward() 
            elif self.curChar == '[':
                tokens.append(Token(T_LSQUARE, pos_start=self.pos))
                self.forward() 
            elif self.curChar == ']':
                tokens.append(Token(T_RSQUARE, pos_start=self.pos))
                self.forward() 
            elif self.curChar == '!':
                tok, error = self.create_not_equal()
                if error: return [], error
                tokens.append(tok) 
            elif self.curChar == '=':
                tokens.append(self.create_equals())
            elif self.curChar == '<':
                tokens.append(self.create_less_than())
            elif self.curChar == '>':
                tokens.append(self.create_greater_than())
            elif self.curChar == ',':
                tokens.append(Token(T_COMMA, pos_start=self.pos))
                self.forward() 
            else:
                pos_start = self.pos.copy()
                char = self.curChar
                self.forward()
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos)

        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens, None

    def create_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False 
        self.forward()

        escape_characters = {
            'n': '\n',
            't': '\t',
            'ב': 'ךלמה יביב',
            'ע': 'הרואמהמ אצ זר יליע'
        }

        while self.curChar != None and (self.curChar != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.curChar, self.curChar)
                escape_character = False
            else:
                if self.curChar == '\\':
                    escape_character = True
                else:
                    string += self.curChar
            self.forward()

        self.forward()
        return Token(T_STRING, string, pos_start, self.pos) 

    def create_minus_or_arrow(self):
        tok_type = T_MINUS
        pos_start = self.pos.copy()
        self.forward()

        if self.curChar == ">":
            self.forward()
            tok_type = T_POINTER
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def create_identifier(self):  
        id_str = ''
        pos_start = self.pos.copy() 

        while self.curChar != None and self.curChar in LETTERS_AND_DIGITS + '_':
            id_str += self.curChar
            self.forward()

        token_type = T_KEYWORD if id_str in KEYWORDS else T_IDENTIFIER
        return Token(token_type, id_str, pos_start, self.pos)

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

    def create_not_equal(self):
        pos_start = self.pos.copy()
        self.forward()

        if self.curChar == "=":
            self.forward()
            return Token(T_NE, pos_start=pos_start, pos_end=self.pos), None

        self.forward()
        return None, ExpectedCharError("ירחא '=' ותל יתיפיצ '!' ", pos_start, self.pos)

    def create_equals(self):
        token_type = T_EQ
        pos_start = self.pos.copy()
        self.forward() 

        if self.curChar == '=':
            self.forward()
            token_type = T_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def create_less_than(self):
        token_type = T_LT
        pos_start = self.pos.copy()
        self.forward() 

        if self.curChar == '=':
            self.forward()
            token_type == T_LTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def create_greater_than(self):
        token_type = T_GT
        pos_start = self.pos.copy()
        self.forward() 

        if self.curChar == '=':
            self.forward()
            token_type == T_GTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

########################
#         Run          #
########################

global_symbols_table = SymbolTable()
global_symbols_table.SetValue('כלום', Number.NULL)
global_symbols_table.SetValue('ליכוד', Number.LIKUD)
global_symbols_table.SetValue('מרצ', Number.MERETZ)

global_symbols_table.SetValue('פאי', Number.math_pi)

global_symbols_table.SetValue('שרה', BuiltInFunction.print)
global_symbols_table.SetValue('תקשורת', BuiltInFunction.input)
global_symbols_table.SetValue('העלם_ראיות', BuiltInFunction.clear)
global_symbols_table.SetValue('האם_שוחד', BuiltInFunction.is_number)
global_symbols_table.SetValue('האם_מחרוזת', BuiltInFunction.is_string)
global_symbols_table.SetValue('האם_רשימה', BuiltInFunction.is_list)
global_symbols_table.SetValue('האם_פונקציה', BuiltInFunction.is_function)
global_symbols_table.SetValue('הוסף', BuiltInFunction.append)
global_symbols_table.SetValue('מחק', BuiltInFunction.remove)
global_symbols_table.SetValue('שלוף', BuiltInFunction.pop)
global_symbols_table.SetValue('הרחב', BuiltInFunction.extend)
global_symbols_table.SetValue('מחרוזת_לרשימה', BuiltInFunction.stringToList)
global_symbols_table.SetValue('מחרוזת_למספר', BuiltInFunction.stringToNumber)
global_symbols_table.SetValue('האם_שמאלני', BuiltInFunction.isLeft)
global_symbols_table.SetValue('אורך', BuiltInFunction.length)

def run(file_name, text):

    # create a lexer object
    lexer = Lexer(file_name, text)
    tokens, error = lexer.create_tokens()
    if error: return None, error

    # create a parser object
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # create interpreter
    interpreter = Interpreter()
    context = Context('~תיסיסבה תינכותה~')
    context.SymbolTable = global_symbols_table
    
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
