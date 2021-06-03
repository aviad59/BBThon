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

    def forward(self):
        self.tok_index += 1
        self.update_current_token()
        return self.cur_token
    
    def backward(self, amount=1):
        self.tok_index -= amount
        self.update_current_token()
        return self.cur_token

    def update_current_token(self):
        if self.tok_index >= 0 and self.tok_index < len(self.tokens):
            self.cur_token = self.tokens[self.tok_index]

    def parse(self):
        res = self.statements()
        if not res.error and self.cur_token.type != T_EOF:
            return res.failure(InvalidSyntaxError("- + / * ) ( == > < >= <=:ב שמתשת השקבב הלועפ אל תאז", self.cur_token.pos_start, self.cur_token.pos_end))
        return res
        
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

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.cur_token.pos_start.copy()

        while self.cur_token.type == T_NEWLINE:
            res.register_forward()
            self.forward()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newlines_count = 0
            while self.cur_token.type == T_NEWLINE:
                res.register_forward()
                self.forward()
                newlines_count += 1
            if newlines_count == 0:
                more_statements = False
            
            if not more_statements: 
                break

            statement = res.try_register(self.statement())
            if not statement:
                self.backward(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(statements, pos_start, self.cur_token.pos_end.copy()))

    def statement(self):
        res = ParseResult()
        pos_start = self.cur_token.pos_start.copy()

        if self.cur_token.match(T_KEYWORD, 'החזר'):
            res.register_forward()
            self.forward()

            expr = res.try_register(self.expression())
            if not expr:
                self.backward(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.cur_token.pos_start.copy()))
        
        if self.cur_token.match(T_KEYWORD, 'המשך'):
            res.register_forward()
            self.forward()
            return res.success(ContinueNode(pos_start, self.cur_token.pos_start.copy()))
        
        if self.cur_token.match(T_KEYWORD, 'הפסק'):
            res.register_forward()
            self.forward()
            return res.success(BreakNode(pos_start, self.cur_token.pos_start.copy()))

        expr = res.register(self.expression())
        if res.error: 
            return res.failure(InvalidSyntaxError(
                '"אל" וא "]", ")", "-", "+", ,"ףדמחומ" ,"דועלכ" ,"ליבשב" ,"םא" ,"דחוש" ,רוצע ,קספה ,ךשמה ,ההזמ ,רפסמל יתיפיצ',pos_start, self.cur_token.pos_end))
        
        return res.success(expr)

    def expression(self):
        res = ParseResult()

        if self.cur_token.match(T_KEYWORD, 'מתנה'):
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
            res.failure(InvalidSyntaxError(
                '"אל" וא "]", ")", "-", "+", ,"ףדמחומ" ,"דועלכ" ,"ליבשב" ,"םא" ,"דחוש" ,ההזמ ,רפסמל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end
                ))

        return res.success(node)
    
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
            return res.failure(InvalidSyntaxError('"אל" וא "]", ")", "-", "+", ,"ףדמחומ" ,"דועלכ" ,"ליבשב" ,"םא" ,ההזמ ,רפסמל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

        return res.success(node)

    def arith_opertion(self):
        return self.extract_op(self.term, (T_PLUS, T_MINUS))
    
    def term(self):
        return self.extract_op(self.factor, (T_MUL, T_DIV, T_DOLLAR))
    
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
    
    def power(self):
        return self.extract_op(self.call, (T_POW, ), self.factor)
    
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        
        if res.error: return res
        
        if self.cur_token.type == T_LPAREN:
            res.register_forward()
            self.forward()
            
            arg_nodes = []
            
            if self.cur_token.type == T_RPAREN:
                res.register_forward()
                self.forward()
            else:
                arg_nodes.append(res.register(self.expression()))
                if res.error: 
                    return res.failure(InvalidSyntaxError(
                        '"אל" וא "]" ")", "(", "-", "+",  ,"ףדמחומ" ,"דועלכ" ,"ליבשב" ,"םא" ,"דחוש" ,ההזמ ,רפסמל יתיפיצ',
                        self.cur_token.pos_start,
                        self.cur_token.pos_end
                    ))
                
                while self.cur_token.type == T_COMMA:
                     res.register_forward()
                     self.forward()
                     
                     arg_nodes.append(res.register(self.expression()))   
                     if res.error: return res

                if self.cur_token.type != T_RPAREN:
                    return res.failure(InvalidSyntaxError('"("-ל וא ","-ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

                res.register_forward()
                self.forward()
                
            return res.success(CallFuncNode(atom, arg_nodes))
        return res.success(atom)
        
    def atom(self):
        res = ParseResult()
        token = self.cur_token

        if token.type in (T_INT, T_FLOAT):
            res.register_forward()
            self.forward()
            return res.success(NumberNode(token))
        
        elif token.type == T_STRING:
            res.register_forward()
            self.forward()
            return res.success(StringNode(token))

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
        
        elif token.type == T_LSQUARE:
            list_expression = res.register(self.list_expression())
            if res.error: return res
            return res.success(list_expression)
        
        elif token.match(T_KEYWORD, 'אם'):
            if_expr = res.register(self.if_expression())
            if res.error: return res
            return res.success(if_expr)

        elif token.match(T_KEYWORD, 'בשביל'):
            for_expr = res.register(self.for_expression())
            if res.error: return res
            return res.success(for_expr)               

        elif token.match(T_KEYWORD, 'כלעוד'):
            while_expr = res.register(self.while_expression())
            if res.error: return res
            return res.success(while_expr)
        
        elif token.match(T_KEYWORD, 'מוחמדף'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def) 

        return res.failure(InvalidSyntaxError('"ףדמחומ" וא "דועלכ" ,"ליבשב" ,"םא" "]", ")", "-", "+", ,ההזמ ,רפסמל יתיפיצ', token.pos_start, token.pos_end))

    def list_expression(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.cur_token.pos_start.copy()
        
        if self.cur_token.type != T_LSQUARE:
            return res.failure(InvalidSyntaxError('"]"-ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
    
        res.register_forward()
        self.forward()
        
        if self.cur_token.type == T_RSQUARE:
            res.register_forward()
            self.forward()
        else:
            element_nodes.append(res.register(self.expression()))
            if res.error: 
                return res.failure(InvalidSyntaxError(
                    '"אל" וא ")" "]", "[", "-", "+",  ,"ףדמחומ" ,"דועלכ" ,"ליבשב" ,"םא" ,"דחוש" ,ההזמ ,רפסמל יתיפיצ',
                    self.cur_token.pos_start,
                    self.cur_token.pos_end
                 ))
                
            while self.cur_token.type == T_COMMA:
                res.register_forward()
                self.forward()
                         
                element_nodes.append(res.register(self.expression()))   
                if res.error: return res

            if self.cur_token.type != T_RSQUARE:
                return res.failure(InvalidSyntaxError('"["-ל וא ","-ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

            res.register_forward()
            self.forward()
    
        return res.success(ListNode(
            element_nodes,
            pos_start,
            self.cur_token.pos_end.copy()
        ))
    
    def if_expression(self):
        res = ParseResult()
        cases_all = res.register(self.if_expression_cases('אם'))
        if res.error: return res
        cases, else_cases = cases_all
        return res.success(IFNode(cases, else_cases))
    
    def if_expression_elif(self):
        return self.if_expression_cases('אחרם')

    def if_expression_else(self):
        res = ParseResult()
        else_case = None     

        if self.cur_token.match(T_KEYWORD, 'אחרת'):
            res.register_forward()
            self.forward()
            
            if self.cur_token.type == T_NEWLINE:
                res.register_forward()
                self.forward()
                
                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.cur_token.match(T_KEYWORD, 'סיום'):
                    res.register_forward()
                    self.forward()
                else:
                    return res.failure(InvalidSyntaxError("!רוגס אל קיתה", self.cur_token.pos_start, self.cur_token.pos_end))
            else:
                expr = res.register(self.statements())
                if res.error: return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expression_else_or_elif(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.cur_token.match(T_KEYWORD, 'אחרם'):
            all_cases = res.register(self.if_expression_elif())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expression_else())
            if res.error: return res
        
        return res.success((cases, else_case))

    def if_expression_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.cur_token.match(T_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(f"'{case_keyword}' יאנתל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()

        condition = res.register(self.expression())
        if res.error: return res

        if not self.cur_token.match(T_KEYWORD, 'אז'):
            return res.failure(InvalidSyntaxError("'זא' יאנתל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()

        if self.cur_token.type == T_NEWLINE:
            res.register_forward()
            self.forward()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.cur_token.match(T_KEYWORD, 'סיום'):
                res.register_forward()
                self.forward()
            else:
                all_cases = res.register(self.if_expression_else_or_elif())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statements())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expression_else_or_elif())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expression(self):
        res = ParseResult()

        if not self.cur_token.match(T_KEYWORD, 'בשביל'):
            return res.failure(InvalidSyntaxError('"ליבשב"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
        
        res.register_forward()
        self.forward()

        if self.cur_token.type != T_IDENTIFIER:
            return res.failure(InvalidSyntaxError("ההזמל יתיפיצ", self.cur_token.pos_start, self.cur_token.pos_end))

        variable_name = self.cur_token
        res.register_forward()
        self.forward()

        if self.cur_token.type != T_EQ:
            return res.failure(InvalidSyntaxError('"=" ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()

        start_value = res.register(self.expression())
        if res.error: return res

        if not self.cur_token.match(T_KEYWORD, 'עד'):
            return res.failure(InvalidSyntaxError('"דע"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
        
        res.register_forward()
        self.forward()

        end_value = res.register(self.expression())
        if res.error: return res

        if self.cur_token.match(T_KEYWORD, 'צעד'):
            res.register_forward()
            self.forward()

            step_value = res.register(self.expression())
            if res.error: return res
        else:
            step_value = None

        if not self.cur_token.match(T_KEYWORD, 'אז'):
            return res.failure(InvalidSyntaxError('"זא"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
        
        res.register_forward()
        self.forward()

        if self.cur_token.type == T_NEWLINE:
            res.register_forward()
            self.forward()

            body = res.register(self.statements())
            if res.error: return res

            if not self.cur_token.match(T_KEYWORD, 'סיום'):
                return res.failure(InvalidSyntaxError('"םויס"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

            res.register_forward()
            self.forward()

            return res.success(ForNode(variable_name, start_value, end_value, step_value, body, True))

        res.register_forward()
        self.forward()

        body = res.register(self.statements())
        if res.error: return res

        return res.success(ForNode(variable_name, start_value, end_value, step_value, body, False))

    def while_expression(self):
        res = ParseResult()

        if not self.cur_token.match(T_KEYWORD, 'כלעוד'):
            return res.failure(InvalidSyntaxError('"דועלכ"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()

        condition = res.register(self.expression())
        if res.error: return res

        if not self.cur_token.match(T_KEYWORD, "אז"):
            return res.failure(InvalidSyntaxError('"זא"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()

        if self.cur_token.type == T_NEWLINE:
            res.register_forward()
            self.forward()

            body = res.register(self.statements())
            if res.error: return res

            if not self.cur_token.match(T_KEYWORD, 'סיום'):
                return res.failure(InvalidSyntaxError('"םויס"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

            res.register_forward()
            self.forward()

            return res.success(WhileNode(condition, body, True))


        body = res.register(self.statements())
        if res.error: return res

        return res.success(WhileNode(condition, body, False))

    def func_def(self):
        res = ParseResult()
        
        if not self.cur_token.match(T_KEYWORD, 'מוחמדף'):
            return res.failure(InvalidSyntaxError('"ףדמחומ"-ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward()
        
        if self.cur_token.type == T_IDENTIFIER:
            var_name_tok = self.cur_token
            res.register_forward()
            self.forward()
            
            if self.cur_token.type != T_LPAREN:
                return res.failure(InvalidSyntaxError('")"-ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
        else:
            var_name_tok = None
            if self.cur_token.type != T_LPAREN:
                return res.failure(InvalidSyntaxError('")"-ל וא ההזמל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
        
        res.register_forward()
        self.forward()
        
        arg_name_toks = []
        
        if self.cur_token.type == T_IDENTIFIER:
            arg_name_toks.append(self.cur_token)
            res.register_forward()
            self.forward()
            
            while self.cur_token.type == T_COMMA:
                res.register_forward()
                self.forward()
                
                if self.cur_token.type != T_IDENTIFIER:
                    return res.failure(InvalidSyntaxError('ההזמל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
        
                arg_name_toks.append(self.cur_token)
                res.register_forward()
                self.forward()
             
            if self.cur_token.type != T_RPAREN:
                return res.failure(InvalidSyntaxError('"("-ל וא ","-ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
        else:
             if self.cur_token.type != T_RPAREN:
                return res.failure(InvalidSyntaxError('"("-ל וא ההזמל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))
         
        res.register_forward()
        self.forward() 
        
        if self.cur_token.type == T_POINTER:
            res.register_forward()
            self.forward()       
            
            body = res.register(self.expression())
            if res.error: return res
            
            return res.success(FunctionNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))

        if self.cur_token.type != T_NEWLINE:
            return res.failure(InvalidSyntaxError('השדח הרושל וא "->"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward() 

        body = res.register(self.statements())
        if res.error: return res

        if not self.cur_token.match(T_KEYWORD, 'סיום'):
            return res.failure(InvalidSyntaxError('"םויס"ל יתיפיצ', self.cur_token.pos_start, self.cur_token.pos_end))

        res.register_forward()
        self.forward() 

        return res.success(FunctionNode(
                var_name_tok,
                arg_name_toks,
                body,
                False
            ))

######################
#    Parse Result    #
######################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_forward_count = 0
        self.forward_count = 0
        self.to_reverse_count = 0

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.forward_count
            return None
        return self.register(res)

    def register_forward(self):
        self.last_registered_forward_count = 1
        self.forward_count += 1      

    def register(self, res): 
        self.last_registered_forward_count = res.forward_count
        self.forward_count += res.forward_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_forward_count == 0:
            self.error = error
        return self