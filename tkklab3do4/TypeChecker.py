from collections import defaultdict
import ast_tree
import tree_printer
from SymbolTable import SymbolTable
from scanner import Scanner
from parser import CalcParser


dict_of_types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

dict_of_types["+"]["int"]["int"] = "int"
dict_of_types["+"]["int"]["float"] = "float"
dict_of_types["+"]["float"]["int"] = "float"
dict_of_types["+"]["float"]["float"] = "float"
dict_of_types["+"]["str"]["str"] = "str"
dict_of_types["+"]["matrix"]["matrix"] = "matrix"

dict_of_types["-"]["int"]["int"] = "int"
dict_of_types["-"]["int"]["float"] = "float"
dict_of_types["-"]["float"]["int"] = "float"
dict_of_types["-"]["float"]["float"] = "float"
dict_of_types["-"]["str"]["str"] = "str"
dict_of_types["-"]["matrix"]["matrix"] = "matrix"

dict_of_types["*"]["int"]["int"] = "int"
dict_of_types["*"]["int"]["float"] = "float"
dict_of_types["*"]["float"]["int"] = "float"
dict_of_types["*"]["float"]["float"] = "float"
dict_of_types["*"]["str"]["int"] = "str"
dict_of_types["*"]["int"]["str"] = "str"
dict_of_types["*"]["matrix"]["matrix"] = "matrix"

dict_of_types["/"]["int"]["int"] = "int"
dict_of_types["/"]["int"]["float"] = "float"
dict_of_types["/"]["float"]["int"] = "float"
dict_of_types["/"]["float"]["float"] = "float"
dict_of_types["/"]["matrix"]["matrix"] = "matrix"


dict_of_types[">"]["int"]["int"] = "bool"
dict_of_types[">"]["int"]["float"] = "bool"
dict_of_types[">"]["float"]["int"] = "bool"
dict_of_types[">"]["float"]["float"] = "bool"

dict_of_types["<"]["int"]["int"] = "bool"
dict_of_types["<"]["int"]["float"] = "bool"
dict_of_types["<"]["float"]["int"] = "bool"
dict_of_types["<"]["float"]["float"] = "bool"

dict_of_types[">="]["int"]["int"] = "bool"
dict_of_types[">="]["int"]["float"] = "bool"
dict_of_types[">="]["float"]["int"] = "bool"
dict_of_types[">="]["float"]["float"] = "bool"

dict_of_types["<="]["int"]["int"] = "bool"
dict_of_types["<="]["int"]["float"] = "bool"
dict_of_types["<="]["float"]["int"] = "bool"
dict_of_types["<="]["float"]["float"] = "bool"

dict_of_types["=="]["int"]["int"] = "bool"
dict_of_types["=="]["int"]["float"] = "bool"
dict_of_types["=="]["float"]["int"] = "bool"
dict_of_types["=="]["float"]["float"] = "bool"

dict_of_types["!="]["int"]["int"] = "bool"
dict_of_types["!="]["int"]["float"] = "bool"
dict_of_types["!="]["float"]["int"] = "bool"
dict_of_types["!="]["float"]["float"] = "bool"

dict_of_types[".+"]["matrix"]["matrix"] = "matrix"
dict_of_types[".-"]["matrix"]["matrix"] = "matrix"
dict_of_types[".*"]["matrix"]["matrix"] = "matrix"
dict_of_types["./"]["matrix"]["matrix"] = "matrix"

dict_of_types["+="]["int"]["int"] = "int"
dict_of_types["+="]["int"]["float"] = "float"
dict_of_types["+="]["float"]["int"] = "float"
dict_of_types["+="]["float"]["float"] = "float"
dict_of_types["+="]["str"]["str"] = "str"
dict_of_types["+="]["matrix"]["matrix"] = "matrix"

dict_of_types["-="]["int"]["int"] = "int"
dict_of_types["-="]["int"]["float"] = "float"
dict_of_types["-="]["float"]["int"] = "float"
dict_of_types["-="]["float"]["float"] = "float"
dict_of_types["-="]["str"]["str"] = "str"
dict_of_types["-="]["matrix"]["matrix"] = "matrix"

dict_of_types["*="]["int"]["int"] = "int"
dict_of_types["*="]["int"]["float"] = "float"
dict_of_types["*="]["float"]["int"] = "float"
dict_of_types["*="]["float"]["float"] = "float"
dict_of_types["*="]["str"]["str"] = "str"
dict_of_types["*="]["matrix"]["matrix"] = "matrix"

dict_of_types["/="]["int"]["int"] = "int"
dict_of_types["/="]["int"]["float"] = "float"
dict_of_types["/="]["float"]["int"] = "float"
dict_of_types["/="]["float"]["float"] = "float"
dict_of_types["/="]["matrix"]["matrix"] = "matrix"


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, ast_tree.Node):
                            self.visit(item)
                elif isinstance(child, ast_tree.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_String(self, node: ast_tree.String):
        return 'str'

    def visit_IntNum(self, node: ast_tree.IntNum):
        return 'int'

    def visit_FloatNum(self, node: ast_tree.FloatNum):
        return 'float'
    
    def visit_Unary(self, node: ast_tree.Unary):
        return self.visit(node.expr)
    
    def visit_Matrix(self, node: ast_tree.Matrix):
        rows = len(node.matrix)
        cols = len(node.matrix[0])
        for i in range(1,rows):
            if node.matrix[i] != cols:
                print("Bad vector sizes")
                return None
        return 'matrix'
    def visit_Id(self, node: ast_tree.Id):
        return self.symbol_table.get(node.id)
    
    def visit_AssignOp(self, node: ast_tree.AssignOp):
        left_id = node.left.id
        val_type = self.visit(node.right)
        if node.op == "=":
            if isinstance(left_id, str):
                self.symbol_table.put(left_id, val_type)
            else:
                self.symbol_table.put(left_id.id, val_type)
            if val_type == "matrix":
                if isinstance(node.right, ast_tree.Unary):
                    self.symbol_table.v_dims[left_id] = node.right.expr.dims[::-1]
                elif isinstance(node.right, ast_tree.MatrixFunc):
                    self.symbol_table.v_dims[left_id] = [node.right.expr, node.right.expr]
                self.symbol_table.v_type[left_id] = "matrix"
        else:
            var_type = self.symbol_table.get(left_id)
            if var_type == 'matrix' and val_type == 'matrix':
                var_dim = self.symbol_table.v_dims[left_id]
                val_dim = node.right.dims
                if var_dim[0] != val_dim[0] or var_dim[1] != val_dim[1]:
                    print("Wrong sizes of matrices")
                    return None
            if dict_of_types[node.op][var_type][val_type] != '':
                return dict_of_types[node.op][var_type][val_type]
            else:
                print("Operation between types not defined")
                return None        

                


    def visit_Function(self, node: ast_tree.MatrixFunc):
        if isinstance(node.expr, int):
            return 'Matrix'
        print("Matrix functions takes only integer arguments!")
        return None

    def visit_Variable(self, node: ast_tree.Variable):
        pass

    def visit_While(self, node: ast_tree.While):
        self.loop_indent += 1
        self.visit(node.cond)
        self.visit(node.instructions)
        self.loop_indent -= 1
    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op

        if dict_of_types[op][type1][type2] == "":
            print(f"Bad types: {type1} {op} {type2})")
            return None
        if type1 == "matrix" or type2 == "matrix":
            return "matrix"
        
if __name__ == '__main__':
    scanner = Scanner()
    parser = CalcParser()
    typeChecker = TypeChecker()
    with open("test.txt", "r") as infile:
        source_code = infile.read()
        infile.close()

    
    ast = parser.parse(scanner.tokenize(source_code))
    ast.printTree(0)
    print(ast)
    typeChecker.visit(ast)
 
            
 

    #def visit_Variable(self, node : ast_tree.Variable):

        