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
    'אחם',
    'אחרת',
]

# Types
T_INT                   = "INT"
T_FLOAT                 = "FLOAT"

# Variables
T_IDENTIFIER            = "IDENTIFIER"
T_KEYWORD               = "KEYWORD"
T_EQ                    = "EQUALS"

# Comparisons
T_EE                   = 'EE'
T_NE					= 'NE'
T_LT					= 'LT'
T_GT					= 'GT'
T_LTE				    = 'LTE'
T_GTE				    = 'GTE'

# Operations
T_PLUS                  = "PLUS"
T_MINUS                 = "MINUS"
T_MUL                   = "MUL"
T_DIV                   = "DIV"

T_POW                   = "POW"

T_LPAREN                = "LPAREN"
T_RPAREN                = "RPAREN"

# Misc
T_EOF                   = "EOF"
