import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

# List of token names
tokens = [
             'ID',
             'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
             'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
             'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',
             'INTNUM',
             'FLOATNUM',
             'STRING'
         ] + list(reserved.values())

# LLiteral characters
literals = ['+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ':', '\'', ',', ';']

# Matrix operators
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

# Assign operators
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

# Relational operators
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Ignore comments
t_ignore_COMMENTS = r'\#.*'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_FLOATNUM(t):
    r'((\d+\.\d*)|(\.\d+))([eE][+-]?\d+)?|(\d+)([eE][+-]?\d+)'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'".*?"'
    t.value = str(t.value)
    return t


# Tracking line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()