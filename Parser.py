from constants import *
from errors import *
from Nodes import *

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