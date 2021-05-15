import string

DIGITS = '1234567890'
LETTERS = string.ascii_letters + "אבגדהוזחטיכלמנסעפצקרשתץףם"
LETTERS_AND_DIGITS = LETTERS + DIGITS

# Keywords
KEYWORDS = [
    'שוחד',
    'וגם',
    'או',
    'לא',
    'אם',
    'אז',
    'אחרם',
    'אחרת',
]

# Types
T_INT = "INT"
T_FLOAT = "FLOAT"

# Variables
T_IDENTIFIER = "IDENTIFIER"
T_KEYWORD = "KEYWORD"
T_EQ = "EQUALS"

# Comparisons
T_EE = "EQUALEQUAL"
T_NE = "NEQUAL"
T_LT = "LTHAN" 
T_GT = "GTHAN"
T_LTE = "LTEQUAL" 
T_GTE = "GTEQUAL"

# Operations
T_PLUS = "PLUS"
T_MINUS = "MINUS"
T_MUL = "MUL"
T_DIV = "DIV"

T_POW = "POW"

T_LPAREN = "LPAREN"
T_RPAREN = "RPAREN"

# Misc
T_EOF = "EOF"
