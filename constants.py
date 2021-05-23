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
    'בשביל',
    'עד',
    'קפוץ',
    'כלעוד',
    'מוחמדף'
]

# Types
T_INT         = "INT"
T_FLOAT       = "FLOAT"
T_STRING      = "STRING"

# Variables
T_IDENTIFIER  = "IDENTIFIER"
T_KEYWORD     = "KEYWORD"
T_EQ          = "EQUALS"

# Comparisons
T_EE          = 'EE'
T_NE          = 'NE'
T_LT          = 'LT'
T_GT          = 'GT'
T_LTE         = 'LTE'
T_GTE         = 'GTE'

# Operations
T_PLUS        = "PLUS"
T_MINUS       = "MINUS"
T_MUL         = "MUL"
T_DIV         = "DIV"
T_POW         = "POW"

T_LPAREN      = "LPAREN"
T_RPAREN      = "RPAREN"

# Functions
T_COMMA       = "COMMA"
T_POINTER     = "ARROW" 

# Misc
T_EOF         = "EOF"
