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
