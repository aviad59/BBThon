from os import error
from constants import *
from errors import *

#######################
#     Symbol Table    #
#######################
class SymbolTable:
    def __init__(self):
        self.local_symbols_dict = {}  
        self.global_symbols_dict = None

    def GetValue(self, name):
        value = self.local_symbols_dict.get(name, None)
        if value == None and self.global_symbols_dict:
           value = self.global_symbols_dict.get(name) 
        return value

    def SetValue(self, name, value):
        self.local_symbols_dict[name] = value

    def remove(self, name):
        del self.local_symbols_dict[name]

#######################
#    Runtime Result   #
#######################
class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

#######################
#       Context       #
#######################

class Context:
    def __init__(self, dis_name, parent=None, parent_position=None):
        self.dis_name = dis_name
        self.parent = parent
        self.parent_position = parent_position
        self.SymbolTable = None


#######################
#        Nodes        #
#######################
class NumberNode:
    def __init__(self, tok):
        self.token = tok
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'
class VariableAccessNode:
    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.pos_start = self.variable_name.pos_start
        self.pos_end = self.variable_name.pos_end
class VariableAssignmentNode:
    def __init__(self, variable_name, value):
        self.variable_name = variable_name 
        self.value_node = value 

        self.pos_start = self.variable_name.pos_start
        self.pos_end = self.variable_name.pos_end
class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.lNode = left_node
        self.op_token = op_token
        self.rNode = right_node
    
        self.pos_start = self.lNode.pos_start
        self.pos_end = self.rNode.pos_end

    def __repr__(self):
        return f'({self.lNode}, {self.op_token}, {self.rNode})'
class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_token}, {self.node})'
class IFNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

####################
#      Parser      #
####################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_index = -1
        self.forward()

    def forward(self, ):
        self.tok_index += 1
        if self.tok_index < len(self.tokens):
            self.cur_token = self.tokens[self.tok_index]
        return self.cur_token

    def parse(self):
        res = self.expression()
        if not res.error and self.cur_token.type != T_EOF:
            return res.failure(InvalidSyntaxError("- + / * ) ( == > < >= <=:ב שמתשת השקבב הלועפ אל תאז", self.cur_token.pos_start, self.cur_token.pos_end))
        return res

    def atom(self):
        res = ParseResult()
        token = self.cur_token

        if token.type in (T_INT, T_FLOAT):
            res.register_forward()
            self.forward()
            return res.success(NumberNode(token))
        
        elif token.type == T_IDENTIFIER:
            res.register_forward()
            self.forward()
            return res.success(VariableAccessNode(token))

        elif token.type == T_LPAREN:
            res.register_forward()
            self.forward()
            expr = res.register(self.expression())
            if res.error: return res
            if self.cur_token.type == T_RPAREN:
                res.register_forward()
                self.forward()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError("םיירגוס תריגסל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        elif token.match(T_KEYWORD, 'אם'):
            if_expr = res.register(self.if_expression())
            if res.error: return res
            return res.success(if_expr)

        return res.failure(InvalidSyntaxError("םיירגוס תחיתפ וא ההזמ ,סונימ ,סולפ ,רפסמל יתיפיצ", token.pos_start, token.pos_end))

    def power(self):
        return self.extract_op(self.atom, (T_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.cur_token

        if tok.type in (T_PLUS, T_MINUS):
            res.register_forward()
            self.forward()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()
 
    def if_expression(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.cur_token.match(T_KEYWORD, 'אם'):
            return res.failure(InvalidSyntaxError("'םא' יאנתל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()

        condition = res.register(self.expression())
        if res.error: return res

        if not self.cur_token.match(T_KEYWORD, 'אז'):
            return res.failure(InvalidSyntaxError("'זא' יאנתל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()

        expr = res.register(self.expression())
        if res.error: return res
        cases.append((condition, expr))

        while self.cur_token.match(T_KEYWORD, 'אחם'):
            res.register_forward()
            self.forward()

            condition = res.register(self.expression())
            if res.error: return res

            if not self.cur_token.match(T_KEYWORD, 'אז'):
                return res.failure(InvalidSyntaxError("'זא' יאנתל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

            res.register_forward()
            self.forward()

            expr = res.register(self.expression())
            if res.error: return res
            cases.append((condition, expr))

        if self.cur_token.match(T_KEYWORD, 'אחרת'):
            res.register_forward()
            self.forward()

            else_case = res.register(self.expression())
            if res.error: return res

        return res.success(IFNode(cases, else_case))

    def term(self):
        return self.extract_op(self.factor, (T_MUL, T_DIV))
    
    def comp_expression(self):
        res = ParseResult()
        if self.cur_token.match(T_KEYWORD, 'לא'):
            op_tok = self.cur_token
            res.register_forward()
            self.forward()

            node = res.register(self.comp_expression())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.extract_op(self.arith_opertion, (T_EE, T_NE, T_LT, T_GT, T_LTE, T_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError("םיירגוס תחיתפ וא 'אל' ,ההזמ ,סונימ ,סולפ ,רפסמל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        return res.success(node)

    def arith_opertion(self):
        return self.extract_op(self.term, (T_PLUS, T_MINUS))

    def expression(self):
        res = ParseResult()

        if self.cur_token.match(T_KEYWORD, 'שוחד'):
            res.register_forward()
            self.forward()

            if self.cur_token.type != T_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    "הנ הנ הנ הנו הקפ הקפ יתלביק ךא ההזמל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end
                ))

            variable_name = self.cur_token
            res.register_forward()
            self.forward()

            if self.cur_token.type != T_EQ:
                return res.failure(InvalidSyntaxError(
                    "הנ הנ הנ הנו הקפ הקפ יתלביק ךא '=' ןמיסל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end
                ))

            res.register_forward()
            self.forward()
            expression = res.register(self.expression())
            if res.error: return res
            return res.success(VariableAssignmentNode(variable_name, expression))

        node = res.register(self.extract_op(self.comp_expression, ((T_KEYWORD, "וגם"), (T_KEYWORD, "או"))))
        if res.error: 
            res.failure(InvalidSyntaxError("םיירגוס תחיתפ וא 'דחוש' ,ההזמ ,סונימ ,סולפ ,רפסמל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        return res.success(node)

    def extract_op(self, func_a, ops, func_b = None):
        if func_b == None:
            func_b = func_a
            
        res = ParseResult()
        left = res.register(func_a())
        
        if res.error: 
            return res

        while self.cur_token.type in ops or (self.cur_token.type, self.cur_token.value) in ops:
            op_tok = self.cur_token
            res.register_forward()
            self.forward()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

######################
#    Parse Result    #
######################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.forward_count = 0

    def register_forward(self):
        self.forward_count += 1      

    def register(self, res): 
        self.forward_count += res.forward_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.forward_count == 0:
            self.error = error
        return self
        

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
            elif self.curChar in DIGITS:
                tokens.append(self.create_number())
            elif self.curChar in LETTERS:
                tokens.append(self.create_identifier())
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
            elif self.curChar == '^':
                tokens.append(Token(T_POW, pos_start=self.pos))
                self.forward() 
            elif self.curChar == '(':
                tokens.append(Token(T_LPAREN, pos_start=self.pos))
                self.forward() 
            elif self.curChar == ')':
                tokens.append(Token(T_RPAREN, pos_start=self.pos))
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
            else:
                pos_start = self.pos.copy()
                char = self.curChar
                self.forward()
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos)

        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens, None

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

    
######################
#       Values       #
######################
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_context(self, context=None):
        self.context = context
        return self

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def substrcted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplyed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError('ץ"גבב קוליח עצבתה',other.pos_start, other.pos_end, self.context)

            return Number(self.value / other.value).set_context(self.context), None

    def powered_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
    
    def get_comparison_eq(self, other):
	    if isinstance(other, Number):
		    return Number(int(self.value == other.value)).set_context(self.context), None

    def get_comparison_ne(self, other):
	    if isinstance(other, Number):
    		return Number(int(self.value != other.value)).set_context(self.context), None

    def get_comparison_lt(self, other):
    	if isinstance(other, Number):
    		return Number(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_gt(self, other):
    	if isinstance(other, Number):
    		return Number(int(self.value > other.value)).set_context(self.context), None

    def get_comparison_lte(self, other):
    	if isinstance(other, Number):
    		return Number(int(self.value <= other.value)).set_context(self.context), None

    def get_comparison_gte(self, other):
    	if isinstance(other, Number):
    		return Number(int(self.value >= other.value)).set_context(self.context), None

    def anded_by(self, other):
    	if isinstance(other, Number):
    		return Number(int(self.value and other.value)).set_context(self.context), None

    def ored_by(self, other):
    	if isinstance(other, Number):
    		return Number(int(self.value or other.value)).set_context(self.context), None

    def notted(self):
    	return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy    

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)


######################
#     Interpreter    #
######################
class Interpreter():
    def visit(self, node, context):
        
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')   

    def visit_NumberNode(self, node, context):
        return RTResult().success(
        Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_VariableAccessNode(self, node, context):
        

        res = RTResult()
        variable_name = node.variable_name.value
        value = context.SymbolTable.GetValue(variable_name)

        if not value:
            return res.failure(RTError(
                f"!םואתפ המ ?המ ?'{variable_name}'", node.pos_start, node.pos_end, context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VariableAssignmentNode(self, node, context):
        res = RTResult()
        variable_name = node.variable_name.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res
        context.SymbolTable.SetValue(variable_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.lNode, context))
        if res.error: return res
        right = res.register(self.visit(node.rNode, context))
        if res.error: return res

        
        if node.op_token.type == T_PLUS:
            result, error = left.added_to(right)
        elif node.op_token.type == T_MINUS:
            result, error = left.substrcted_by(right)
        elif node.op_token.type == T_MUL:
            result, error = left.multiplyed_by(right)
        elif node.op_token.type == T_DIV:
            result, error = left.divided_by(right)
        elif node.op_token.type == T_POW:
            result, error = left.powered_by(right)
        elif node.op_token.type == T_EE:
    	    result, error = left.get_comparison_eq(right)
        elif node.op_token.type == T_NE:
        	result, error = left.get_comparison_ne(right)
        elif node.op_token.type == T_LT:
        	result, error = left.get_comparison_lt(right)
        elif node.op_token.type == T_GT:
        	result, error = left.get_comparison_gt(right)
        elif node.op_token.type == T_LTE:
        	result, error = left.get_comparison_lte(right)
        elif node.op_token.type == T_GTE:
        	result, error = left.get_comparison_gte(right)
        elif node.op_token.match(T_KEYWORD, 'וגם'):
        	result, error = left.anded_by(right)
        elif node.op_token.match(T_KEYWORD, 'או'):
        	result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_token.type == T_MINUS:
            number, Error = number.multiplyed_by(Number(-1))
        elif node.op_token.match(T_KEYWORD, 'לא'):
            number, error = number.notted()
        
        if error: 
            res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IFNode(self, node , context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res
             
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)

            if node.else_case:
                else_value = res.register(self.visit(node.else_case, context))
                if res.error: return res 
                return res.success(else_value)

            return res.success(None)

########################
#         Run          #
########################

global_symbols_table = SymbolTable()
global_symbols_table.SetValue('כלום', Number(0))
global_symbols_table.SetValue('ליכוד', Number(1))
global_symbols_table.SetValue('מרצ', Number(0))

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
    context = Context('~תיסיסבה תינכות~')
    context.SymbolTable = global_symbols_table
    
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
