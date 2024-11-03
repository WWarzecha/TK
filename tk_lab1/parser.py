# parser.py
from sly import Parser
from lexer import Scanner  # Assuming your lexer code is in lexer.py

class MatrixParser(Parser):
    tokens = Scanner.tokens

    variables = {}


    @_('expr "+" term')
    def expr(self,p):
        return p.expr + p.term
    
    @_('term')
    def expr(self,p):
        return p.term


    # Error handling
    def error(self, p):
        if p:
            print(f"Błąd parsowania w linii {p.lineno}: niepoprawny token '{p.value}'")
        else:
            print(f"Błąd parsowania na końcu pliku")

if __name__ == '__main__':
    lexer = Scanner()
    parser = MatrixParser()

    # Read from file
    try:
        #filename = sys.argv[1] if len(sys.argv) > 1 else "full_example.txt"
        #with open(filename, "r") as file:
            #text = file.read()
        text = "A = zeros(5);"
        # Parse the input
        result = parser.parse(lexer.tokenize(text))
        print(result)  # Print the parse tree or any result structure

    except IOError:
        print(f"Nie można otworzyć pliku: {filename}")
