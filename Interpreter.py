from Parser import *

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
