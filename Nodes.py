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
class StringNode:
    def __init__(self, tok):
        self.token = tok

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'
class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end
        
    def __repr__(self):
        return f'{self.element_nodes}'
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
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end
class ForNode:
    def __init__(self, variable_name_token, start_value, end_value, step_value, body_node, return_null):
        self.variable_name_token = variable_name_token
        self.start_value = start_value
        self.end_value = end_value
        self.step_value = step_value
        self.body_node = body_node
        self.return_null = return_null
        
        self.pos_start = self.variable_name_token.pos_start
        self.pos_end = self.body_node.pos_end
class WhileNode:
    def __init__(self, condition_node, body_node, return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.return_null = return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end
class FunctionNode:
    def __init__(self, variable_name_token, arg_name_tokens, body_node, return_auto):
        self.var_name_tok = variable_name_token
        self.arg_name_toks = arg_name_tokens
        self.body_node = body_node

        self.return_auto = return_auto

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end
class CallFuncNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_node = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_node) > 0:
            self.pos_end = self.arg_node[len(self.arg_node) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
class ReturnNode:
    def __init__(self, return_node, pos_start, pos_end):
        self.return_node = return_node
        self.pos_start = pos_start
        self.pos_end = pos_end
class ContinueNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
 