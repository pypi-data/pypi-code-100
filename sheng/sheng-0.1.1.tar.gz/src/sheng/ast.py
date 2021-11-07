from abc import *
from .symtable import *
from .exception import *


class Node(ABC):

    def evaluate(self, symtable):
        raise NotImplementedError()


class NodeSequence(Node):

    def __init__(self, sequence):
        self._sequence = sequence
        self._index = -1

    def __getitem__(self, index):
        return self._sequence[index]

    def __len__(self):
        return len(self._sequence)

    def __iter__(self):
        return iter(self._sequence)


class Program(Node):

    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, symtable):
        return self.statements.evaluate(symtable)


class Statement(Node): pass


class StatementSequence(NodeSequence):

    def evaluate(self, symtable):
        for node in self._sequence:
            value = node.evaluate(symtable)
            if (value):
                return value
        return None


class FunctionDef(Statement):

    def __init__(self, name, arguments, body):
        self.name = name
        self.arguments = arguments
        self.body = body

    def evaluate(self, symtable):
        identifier = self.name.get_identifier()
        symtable.insert(identifier, self)
        return None

    def get_arguments(self):
        return self.arguments

    def get_body(self):
        return self.body


class ArgumentSequence(NodeSequence): pass


class Return(Statement):

    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, symtable):
        value = self.expression.evaluate(symtable)
        ReturnValue = type('ReturnValue', (type(value), ), {})
        return ReturnValue(value)


class Print(Statement):

    def __init__(self, node):
        self.node = node

    def evaluate(self, symtable):
        value = self.node.evaluate(symtable)
        if (type(value) == bool):
            value = '对' if value else '错'
        print(value)
        return None


class Assignment(Statement):

    def __init__(self, name, node):
        self.name = name
        self.node = node

    def evaluate(self, symtable):
        identifier = self.name.get_identifier()
        node = Constant(self.node.evaluate(symtable))
        symtable.insert(identifier, node)
        return None


class If(Statement):

    def __init__(self, expression, statements, elifs):
        self.expression = expression
        self.statements = statements
        self.elifs = elifs

    def evaluate(self, symtable):
        if (self.expression.evaluate(symtable)):
            return self.statements.evaluate(symtable)
        else:
            return self.elifs.evaluate(symtable)


class ElifSequence(NodeSequence):

    def __init__(self, sequence, statements_else=None):
        super().__init__(sequence)
        self.statements_else = statements_else

    def evaluate(self, symtable):
        for expression, statements in self._sequence:
            if (expression.evaluate(symtable)):
                return statements.evaluate(symtable)
        if (self.statements_else):
            return self.statements_else.evaluate(symtable)
        return None


class Iterate(Statement):

    def __init__(self, identifier, iterable, statements):
        self.identifier = identifier
        self.iterable = iterable
        self.statements = statements

    def evaluate(self, symtable):
        for e in self.iterable.evaluate(symtable):
            node = Constant(e)
            symtable.insert(self.identifier, node)
            value = self.statements.evaluate(symtable)
            if (type(value).__name__ == 'ReturnValue'):
                return value
            if (type(value).__name__ == 'ContinueValue'):
                continue
            if (type(value).__name__ == 'BreakValue'):
                break
        return None


class Loop(Statement):

    def __init__(self, expression, statements):
        self.expression = expression
        self.statements = statements

    def evaluate(self, symtable):
        while (self.expression.evaluate(symtable)):
            value = self.statements.evaluate(symtable)
            if (type(value).__name__ == 'ReturnValue'):
                return value
            if (type(value).__name__ == 'ContinueValue'):
                continue
            if (type(value).__name__ == 'BreakValue'):
                break
        return None


class Continue(Statement):

    def evaluate(self, symtable):
        ContinueValue = type('ContinueValue', (object, ), {})
        return ContinueValue()


class Break(Statement):

    def evaluate(self, symtable):
        BreakValue = type('BreakValue', (object, ), {})
        return BreakValue()


class Expression(Node): pass


class ExpressionSequence(NodeSequence): pass


class Constant(Expression):

    def __init__(self, value):
        self.value = value

    def evaluate(self, symtable):
        return self.value


class Boolean(Constant):

    def evaluate(self, symtable):
        return bool(self.value)


class Integer(Constant):

    def evaluate(self, symtable):
        return int(self.value)


class Float(Constant):

    def evaluate(self, symtable):
        return float(self.value)


class Complex(Constant):

    def evaluate(self, symtable):
        return complex(self.value)


class String(Constant):

    def evaluate(self, symtable):
        return str(self.value)


class UnaryOp(Expression):

    def __init__(self, node):
        self.node = node


class Not(UnaryOp):

    def evaluate(self, symtable):
        value = self.node.evaluate(symtable)
        return not value


class USubtract(UnaryOp):

    def evaluate(self, symtable):
        value = self.node.evaluate(symtable)
        return +value


class UAdd(UnaryOp):

    def evaluate(self, symtable):
        value = self.node.evaluate(symtable)
        return -value


class BinaryOp(Expression):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue + rvalue


class Subtract(BinaryOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue - rvalue


class Multiply(BinaryOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue * rvalue


class Divide(BinaryOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue / rvalue


class Modulo(BinaryOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue % rvalue


class Power(BinaryOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue ** rvalue


class FloorDivide(BinaryOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue // rvalue


class BoolOp(BinaryOp): pass


class And(BoolOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue and rvalue


class Or(BoolOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue or rvalue


class CompareOp(BinaryOp): pass


class Equal(CompareOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue == rvalue


class NotEqual(CompareOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue != rvalue


class Less(CompareOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue < rvalue


class LessEqual(CompareOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue <= rvalue


class Greater(CompareOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue > rvalue


class GreaterEqual(CompareOp):

    def evaluate(self, symtable):
        lvalue = self.left.evaluate(symtable)
        rvalue = self.right.evaluate(symtable)
        return lvalue >= rvalue


class Name(Expression):

    def __init__(self, value):
        self.value = value

    def get_identifier(self):
        return self.value
    
    def evaluate(self, symtable):
        symbol = symtable.lookup(self.value)
        node = symbol.get_node()
        return node.evaluate(symtable)


class FunctionCall(Expression):

    def __init__(self, name, expressions):
        self.name = name
        self.expressions = expressions
    
    def evaluate(self, symtable):
        identifier = self.name.get_identifier()
        symbol = symtable.lookup(identifier)
        if (not isinstance(symbol.get_node(), FunctionDef)):
            raise RuntimeException(f'{identifier} is not a function')

        # Get function definition and its attributes
        functiondef = symbol.get_node()
        arguments = functiondef.get_arguments()
        body = functiondef.get_body()

        # Create child symbol table and insert parent symbols
        function_symtable = Function(arguments, body)
        symbols = symtable.to_dict()
        for _, s in symbols.items():
            function_symtable.insert(s.get_identifier(), s.get_node())

        # Assign values to arguments respectively
        for i in range(len(self.expressions)):
            arg_identifier = arguments[i].get_identifier()
            arg_node = Constant(self.expressions[i].evaluate(symtable))
            function_symtable.insert(arg_identifier, arg_node)
        
        # Evaluate statements in body
        value = body.evaluate(function_symtable)
        if (type(value).__name__ == 'ReturnValue'):
            return value
        return None


class Iterable(Constant): pass


class ArrayList(Iterable):

    def __init__(self, expressions):
        self.expressions = expressions
    
    def evaluate(self, symtable):
        return [
            expression.evaluate(symtable) 
            for expression in self.expressions
        ]


class IterableIndex(Expression):

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def evaluate(self, symtable):
        iterable = self.name.evaluate(symtable)
        index = self.expression.evaluate(symtable)
        return iterable[index]
