from typing import Text
from Parser import *

import os
import math

######################
#     Interpreter    #
######################
class Interpreter:
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

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
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
        elif node.op_token.type == T_DOLLAR:
            result, error = left.dollar_index(right)
        elif node.op_token.type == T_POW:
            result, error = left.powered_by(right)
        elif node.op_token.type == T_EE:
    	    result, error = left.GetValue_comparison_eq(right)
        elif node.op_token.type == T_NE:
        	result, error = left.GetValue_comparison_ne(right)
        elif node.op_token.type == T_LT:
        	result, error = left.GetValue_comparison_lt(right)
        elif node.op_token.type == T_GT:
        	result, error = left.GetValue_comparison_gt(right)
        elif node.op_token.type == T_LTE:
        	result, error = left.GetValue_comparison_lte(right)
        elif node.op_token.type == T_GTE:
        	result, error = left.GetValue_comparison_gte(right)
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

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value, context))
        if res.error: return res

        end_value = res.register(self.visit(node.end_value, context))
        if res.error: return res

        if node.step_value:
            step_value = res.register(self.visit(node.step_value, context))
            if res.error: return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.SymbolTable.SetValue(node.variable_name_token.value, Number(i))
            i += step_value.value

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res
        
        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.is_true(): break

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res

        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_FunctionNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.SymbolTable.SetValue(func_name, func_value)

        return res.success(func_value)

    def visit_CallFuncNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_node:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
        
    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res
        
        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

#######################
#     Symbol Table    #
#######################
class SymbolTable:
    def __init__(self, parent=None):
        self.local_symbols_dict = {}  
        self.global_symbols_dict = parent

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
#       Context       #
#######################
class Context:
    def __init__(self, dis_name, parent=None, parent_position=None):
        self.dis_name = dis_name
        self.parent = parent
        self.parent_position = parent_position
        self.SymbolTable = None

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
class Value:

    def __init__(self):
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
        return None, self.illegal_operation(other)

    def substrcted_by(self, other):
        return None, self.illegal_operation(other)

    def multiplyed_by(self, other):
        return None, self.illegal_operation(other)

    def divided_by(self, other):
        return None, self.illegal_operation(other)

    def dollar_index(self, other):
        return None, self.illegal_operation(other)

    def powered_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
	    return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
	    return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
    	return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
    	return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
    	return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
    	return None, self.illegal_operation(other)
    
    def anded_by(self, other):
    	return None, self.illegal_operation(other)

    def ored_by(self, other):
    	return None, self.illegal_operation(other)

    def notted(self):
    	return None, self.illegal_operation()

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError("(תרחא חכוה אל דוע לכ הרואכל) תיקוח אל הלועפ", self.pos_start, other.pos_end, self.context)

class Number(Value):
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
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def substrcted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def multiplyed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError('ץ"גבב קוליח עצבתה',other.pos_start, other.pos_end, self.context)
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def powered_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)
    
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def get_comparison_lt(self, other):
    	if isinstance(other, Number):
    		return Number(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
    	    return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, self.pos_end)

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

class String(Value):
    def __init__(self, value):
        super().__init__()    
        self.value = value
    
    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multiplyed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements    

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def substrcted_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError("חווטל ץוחמ אוה יכ הזה סקדניאב רביאה תא קוחמל ןתינ אל", self.pos_start, self.pos_end, self.context)
        else:
            return None, Value.illegal_operation(self, other)

    def multiplyed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            new_list.elements = new_list.elements * other.value
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def dollar_index(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError("חווטל ץוחמ אוה יכ הזה סקדניאב רביאה תא לבקל ןתינ אל", self.pos_start, self.pos_end, self.context)
        else:
            return None, Value.illegal_operation(self, other) 

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f'{", ".join([str(x) for x in self.elements])}'

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<ימינונא>" 

    def create_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start) 
        new_context.SymbolTable = SymbolTable(new_context.parent.SymbolTable)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(f"({len(arg_names) - len(args)}) ולבקתה םיכרע ידמ רתוי", 
            self.pos_start, self.pos_end, self.context))
        
        if len(args) < len(arg_names):
            return res.failure(RTError(f"({len(arg_names) - len(args)}) ולבקתה םיכרע ידמ תצק", 
            self.pos_start, self.pos_end, self.context))

        return res.success(None)
    
    def populate_args(self, args_names, args, exectue_context):
        for i in range(len(args)):
            arg_name = args_names[i]
            arg_value = args[i]
            arg_value.set_context(exectue_context)
            exectue_context.SymbolTable.SetValue(arg_name, arg_value)
    
    def check_and_populate(self, arg_names, args, exectue_context):
        res = RTResult()

        res.register(self.check_args(arg_names, args))
        if res.error: return res
        self.populate_args(arg_names, args, exectue_context)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()

        exec_context = self.create_new_context()

        res.register(self.check_and_populate(self.arg_names, args, exec_context))
        if res.error: return 

        value = res.register(interpreter.visit(self.body_node, exec_context)) 
        if res.error: return res
        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'<{self.name} הייצקנופ>'

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    
    def execute(self, args):
        res = RTResult()
        exec_context = self.create_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit)
        
        res.register(self.check_and_populate(method.arg_names, args, exec_context))
        if res.error: return res

        return_value = res.register(method(exec_context))
        if res.error: return res

        return res.success(return_value)

    def execute_print(self, exec_context):
        print(str(exec_context.SymbolTable.GetValue('value')))
        return RTResult().success(String(str(exec_context.SymbolTable.GetValue('value'))))
    execute_print.arg_names = ['value']

    def execute_input(self, exec_context):
        text = input()
        return RTResult().success(String(text))
    execute_input.arg_names = []

    def execute_clear(self, exec_context):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Number.NULL)
    execute_clear.arg_names = []

    def execute_is_number(self, exec_context):
        is_number = isinstance(exec_context.SymbolTable.GetValue('value'), Number)
        return RTResult().success(Number.LIKUD if is_number else Number.MERETZ)
    execute_is_number.arg_names = ['value']

    def execute_is_string(self, exec_context):
        is_string = isinstance(exec_context.SymbolTable.GetValue('value'), String)
        return RTResult().success(Number.LIKUD if is_string else Number.MERETZ)
    execute_is_string.arg_names = ['value']

    def execute_is_list(self, exec_context):
        is_list = isinstance(exec_context.SymbolTable.GetValue('value'), List)
        return RTResult().success(Number.LIKUD if is_list else Number.MERETZ)
    execute_is_list.arg_names = ['value']

    def execute_is_function(self, exec_context):
        is_function = isinstance(exec_context.SymbolTable.GetValue('value'), BaseFunction)
        return RTResult().success(Number.LIKUD if is_function else Number.MERETZ)
    execute_is_function.arg_names = ['value']

    def execute_append(self, exec_context):
        list_ = exec_context.SymbolTable.GetValue('list')
        value = exec_context.SymbolTable.GetValue('value')

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                "המישר תויהל בייח ןושארה טלקה", self.pos_start, self.pos_end, exec_context
            ))

        list_.elements.append(value)
        return RTResult().success(List(list_.elements))
    execute_append.arg_names = ['list', 'value']

    def execute_remove(self, exec_context):
        list_ = exec_context.SymbolTable.GetValue('list')
        index = exec_context.SymbolTable.GetValue('index') 

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                "המישר תויהל בייח ןושארה טלקה", self.pos_start, self.pos_end, exec_context
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                "רפסמ תויהל בייח ינשה טלקה", self.pos_start, self.pos_end, exec_context
            ))
        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError("חווטל ץוחמ אוה יכ הזה םוקימב רביאה תא לבקל ןתינ אל", self.pos_start, self.pos_end, self.context))
        
        return RTResult().success(element)
    execute_remove.arg_names = ['list', 'index']

    def execute_pop(self, exec_context):
        list_ = exec_context.SymbolTable.GetValue('list')

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                "המישר תויהל בייח ןושארה טלקה", self.pos_start, self.pos_end, exec_context
            ))

        try:
            element = list_.elements.pop(0)
        except:
            return RTResult().failure("חווטל ץוחמ אוה יכ הזה סקדניאב רביאה תא לבקל ןתינ אל", self.pos_start, self.pos_end, self.context)
        
        return element
    execute_pop.arg_names = ['list']

    def execute_extend(self, exec_context):
        list1 = exec_context.SymbolTable.GetValue('list1')
        list2 = exec_context.SymbolTable.GetValue('list2')

        if not isinstance(list1, List):
            return RTResult().failure(RTError(
                "המישר תויהל בייח ןושארה טלקה", self.pos_start, self.pos_end, exec_context
            ))

        if not isinstance(list2, List):
            return RTResult().failure(RTError(
                "המישר תויהל בייח ינשה טלקה", self.pos_start, self.pos_end, exec_context
            ))

        list1.elements.extend(list2.elements)
        return RTResult().success(List(list1.elements))
    execute_extend.arg_names = ['list1', 'list2']

    def execute_stringToList(self, exec_context):
        st = exec_context.SymbolTable.GetValue('string')

        if not isinstance(st, String):
            return RTResult().failure(RTError(
                "תזורחמ תויהל בייח ןושארה טלקה", self.pos_start, self.pos_end, exec_context
            ))

        str_ = ""

        for i in range(len(st.value)):
            str_ += str(st.value[i])
        
        return RTResult().success(List(str_))
    execute_stringToList.arg_names = ['string']

    def execute_isLeft(self, exec_context):
        var = exec_context.SymbolTable.GetValue('string')
        if not isinstance(var, String):
            return RTResult().failure(RTError(
                "תזורחמ תויהל בייח טלקה", self.pos_start, self.pos_end, exec_context
            ))

        if "לאמש" in var.value or "תפתושמה" in var.value or "צרמ" in var.value or "דיפל" in var.value:
            return RTResult().success(Number.LIKUD)
        else:
            return RTResult().success(Number.MERETZ)
    execute_isLeft.arg_names = ['string']

    def no_visit(self):
        raise Exception(f'No execute_{self.name} method defined')
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'<{self.name} תנבומ הייצקנופ>'

#######################
#      Constants      #
#######################

Number.NULL = Number(0)
Number.LIKUD = Number(1)
Number.MERETZ = Number(0)

Number.math_pi = Number(math.pi)

BuiltInFunction.print           = BuiltInFunction("print")
BuiltInFunction.input           = BuiltInFunction("input")
BuiltInFunction.clear           = BuiltInFunction("clear")
BuiltInFunction.is_number       = BuiltInFunction("is_number")
BuiltInFunction.is_string       = BuiltInFunction("is_string")
BuiltInFunction.is_list         = BuiltInFunction("is_list")
BuiltInFunction.is_function     = BuiltInFunction("is_function")
BuiltInFunction.append          = BuiltInFunction("append")
BuiltInFunction.remove          = BuiltInFunction("remove")
BuiltInFunction.pop             = BuiltInFunction("pop")
BuiltInFunction.extend          = BuiltInFunction("extend")
BuiltInFunction.stringToList    = BuiltInFunction("stringToList")
BuiltInFunction.isLeft          = BuiltInFunction("isLeft")

