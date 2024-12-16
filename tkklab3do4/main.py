#object oriented version
from scanner import Scanner
from parser import CalcParser
from TypeChecker import TypeChecker
from sly.lex import LexError
from tree_printer import TreePrinter

if __name__ == '__main__':
    scanner = Scanner()
    parser = CalcParser()
    type_checker = TypeChecker()

    with open("example1.m", "r") as infile:
        source_code = infile.read()
        infile.close()

    try:
        parser.parse(Scanner().tokenize(source_code))
    except LexError as e:
        print(f"Lexer error: {e}")


