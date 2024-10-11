# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer
# tokens =    {BINPLUS, BINMINUS, BINMULT, BINDIV,    # Binary operators
#             MATPLUS, MATMINUS, MATMULT, MATDIV,     # Matrix operators
#             EQ, PLUSEQ, MINEQ, MULTEQ, DICEQ,       # Assign operators
#             # Relational operators
          
          
#           }
class CalcLexer(Lexer):
    tokens = {ID, FLOAT, NUMBER}
    ignore = ' \t'
    literals ='+-*/=<>()[}{]:\',;'
    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    # ID['if'] = 'IF'
    FLOAT = r'\d+\.\d+'
    NUMBER = r'\d+'

    # Special symbols
    # PLUS = r'\+'
    # MINUS = r'-'
    # TIMES = r'\*'
    # DIVIDE = r'/'
    # ASSIGN = r'='
    # LPAREN = r'\('
    # RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

if __name__ == '__main__':
    lexer = CalcLexer()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            for e in lexer.tokenize(text):
                print("(",e.lineno,"): ",e.type,"(",e.value,")",sep="")