import sys
from colorsys import ONE_SIXTH
from idlelib.autocomplete import FORCE

from sly import Lexer


class Scanner(Lexer):
    tokens = {
        ID, INTNUM, FLOAT, STRING, IF, ELSE, WHILE, FOR,
        EYE, ZEROS, ONES, PRINT,
        ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
        LESS, GREATER, LESSEQ, GREATEREQ,
        NOTEQ, EQEQ, DOTADD, DOTSUB, DOTMUL, DOTDIV
    }

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

    literals = {'=', '+', '-', '*', '/', '(', ')', '[', ']', '{', '}', ',', ';', '\'', '<', '>'}

    STRING = r'\".*?\"'
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    # Assignment operators
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='

    # Relational operators
    LESSEQ = r'<='
    GREATEREQ = r'>='
    NOTEQ = r'!='
    EQEQ = r'=='

    # String containing ignored characters (between tokens)
    ignore = ' \t'

    # Other ignored patterns
    ignore_comment = r'\#.*'

    # Extra action for newlines
    @_(r'[\r\n]+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)

    @_(r'(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')
    def FLOAT(self, t):
        t.value = float(t.value)
    

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "full_example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print("(",tok.lineno,"): ", tok.type, "(", tok.value, ")", sep="")