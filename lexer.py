import sys
from colorsys import ONE_SIXTH
from idlelib.autocomplete import FORCE

from sly import Lexer


class Scanner(Lexer):
    tokens = { ID, INTNUM, FLOAT, IF, ELSE, WHILE, FOR, EYE, ZEROS, ONES, PRINT, PLUSASSIGN, MINUSASSIGN,
        TIMESASSIGN, DIVIDEASSIGN,
        LESS, GREATER, LESSEQ, GREATEREQ,
        NOTEQ, EQEQ }

    # Regular expression rules for tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['for'] = FOR
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    literals = {'=', '+', '-', '*', '/', '(', ')',';', '\''}

    FLOAT = r'\d*\.\d+'
    INTNUM = r'\d+'
    # MPLUS = r'.+'
    # MMINUS = r'.-'
    # MTIMES = r'.\*'
    # MDIVIDE = r'./'

    # Assignment operators
    PLUSASSIGN = r'\+='
    MINUSASSIGN = r'-='
    TIMESASSIGN = r'\*='
    DIVIDEASSIGN = r'/='

    # Relational operators
    LESS = r'<'
    GREATER = r'>'
    LESSEQ = r'<='
    GREATEREQ = r'>='
    NOTEQ = r'!='
    EQEQ = r'=='


    # String containing ignored characters (between tokens)
    ignore = ' \t'

    # Other ignored patterns
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print("(",tok.lineno,"): ", tok.type, "(", tok.value, ")", sep="")