from sly import Parser
from scanner import Scanner
from sly.lex import LexError
import ast_tree

def print_error(p, message):
    p = p.error
    
    print("Syntax error in {0}, at line {1}: LexToken({2}, '{3}')".format(message, p.lineno, p.type, p.value))

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ('right', IFX),
        ('right', ELSE),
        ('nonassoc', GREATEREQUAL, LESSEREQUAL, GREATER, LESSER, NOTEQUAL, EQUAL),
        ('left', AND, OR, XOR),
        ('left', "+", "-", DOTADD, DOTSUB),
        ('left', "*", "/", DOTMUL, DOTDIV),
        ('right', NOT, UMINUS),
    )

    start = 'program'

    @_('instructions', '')
    def program(self, p):
        if p[0]=='':
            return ast_tree.Instructions([])
        return ast_tree.Instructions(p[0])

    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        return p[0] + p[1] if len(p) == 2 else p[0]



    @_('if_i',
       'return_i ";"',
       'break_i ";"',
       'continue_i ";"',
       'for_l',
       'while_l',
       'assign ";"',
       'print_i ";"')
    def instruction(self, p):
        return [p[0]]

    @_('"{" instructions "}"')
    def instruction(self, p):
        return p[1]

    @_('STRING')
    def expr(self, p):
        return ast_tree.String(p[0])

    @_('INTNUM')
    def expr(self, p):
        return ast_tree.IntNum(p[0])

    @_('FLOATNUM')
    def expr(self, p):
        return ast_tree.FloatNum(p[0])

    @_('var')
    def expr(self, p):
        return p[0]

    @_('"(" expr ")"')
    def expr(self, p):
        return p[1]

    @_('matrix_element')
    def var(self, p):
        return p[0]

    @_('ID')
    def var(self, p):
        return ast_tree.Id(p[0])

    @_('ID "[" expr "," expr "]"')
    def matrix_element(self, p):
        return ast_tree.Variable(ast_tree.Id(p[0]), (p[2], p[4]))

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',

       'expr EQUAL expr',
       'expr NOTEQUAL expr',
       'expr GREATER expr',
       'expr LESSER expr',
       'expr GREATEREQUAL expr',
       'expr LESSEREQUAL expr',

       'expr DOTMUL expr',
       'expr DOTDIV expr',
       'expr DOTADD expr',
       'expr DOTSUB expr',

       'expr XOR expr',
       'expr AND expr',
       'expr OR expr'
       )
    def expr(self, p):
        return ast_tree.BinExpr(p[0], p[1], p[2])

    @_('var "=" expr',
       'var ADDASSIGN expr',
       'var SUBASSIGN expr',
       'var MULASSIGN expr',
       'var DIVASSIGN expr')
    def assign(self, p):
        return ast_tree.AssignOp(p[0], p[1], p[2])


    @_("unary")
    def expr(self, p):
        return p[0]

    @_('"-" expr %prec UMINUS')
    def unary(self, p):
        return ast_tree.Unary("UMINUS", p[1])

    @_('NOT expr %prec NOT')
    def unary(self, p):
        return ast_tree.Unary("NOT", p[1])

    @_('matrix')
    def expr(self, p):
        return p[0]

    @_('"[" vectors "]"')
    def matrix(self, p):
        return ast_tree.Matrix(p[1])

    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        return p[0] + [p[2]] if len(p) == 3 else [p[0]]

    @_('"[" variables "]"')
    def vector(self, p):
        return p[1]

    @_('variables "," variable',
       'variable')
    def variables(self, p):
        return p[0] + [p[2]] if len(p) == 3 else [p[0]]

    @_('expr')
    def variable(self, p):
        return p[0]
    @_('mat_fun "(" expr ")"')
    def expr(self, p):
        return ast_tree.MatrixFunc(p[0], p[2])

    @_('ZEROS',
       'EYE',
       'ONES')
    def mat_fun(self, p):
        return p[0]

# instrukcje wartunkowe
    @_('IF "(" expr ")" instruction %prec IFX',
       'IF "(" expr ")" instruction ELSE instruction')
    def if_i(self, p):
        return ast_tree.If(p[2], ast_tree.Instructions(p[4])) if len(p) == 5 else ast_tree.If(p[2], ast_tree.Instructions(p[4]), ast_tree.Instructions(p[6]))

#pętle
    @_('WHILE "(" expr ")" instruction')
    def while_l(self, p):
        return ast_tree.While(p[2], ast_tree.Instructions(p[4]))

    @_('FOR ID "=" expr ":" expr instruction', )
    def for_l(self, p):
        return ast_tree.For(ast_tree.Id(p[1]), p[3], p[5], ast_tree.Instructions(p[6]))

    @_('RETURN',
       'RETURN expr')
    def return_i(self, p):
        return ast_tree.Return(p[1]) if len(p) == 2 else ast_tree.Return()

    @_('BREAK')
    def break_i(self,p):
        return ast_tree.Break()
    @_('CONTINUE')
    def continue_i(self,p):
        return ast_tree.Continue()
# print
    @_('PRINT printargs')
    def print_i(self,p):
        return ast_tree.Print(p[1])

    @_('expr "," printargs',
       'expr')
    def printargs(self, p):
        return [p[0]] + p[2] if len(p) == 3 else [p[0]]

    @_('ID "[" expr ":" expr "]"',
       'ID "[" expr ":" expr "," expr ":" expr "]"',  
       'ID "[" ":" expr "]"',
       'ID "[" expr ":" "]"')
    def variable(self, p):
        if len(p) == 6:
            return ast_tree.Variable(ast_tree.Id(p[0]), (p[2], p[4]))
        if len(p) == 10:
            return ast_tree.Variable(ast_tree.Id(p[0]), ((p[2], p[4]), (p[6], p[8])))
        else:
            if p[2] == ":":
                return ast_tree.Variable(ast_tree.Id(p[0]), (ast_tree.IntNum(0), p[3]))
            return ast_tree.Variable(ast_tree.Id(p[0]), (p[2], ast_tree.IntNum(-1)))

if __name__ == '__main__':
    scanner = Scanner()
    parser = CalcParser()
    with open("test.txt", "r") as infile:
        source_code = infile.read()
        infile.close()

    try:
        res = parser.parse(scanner.tokenize(source_code))
        if res is not None:
            res.printTree(0)
    except LexError as e:
        print(f"Lexer error: {e}")