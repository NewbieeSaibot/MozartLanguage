import mozart_parser
import mozart_builtin_functions
from mozart_ast import ASTNode, ASTNodeType, ValueType
from mozart_exceptions import *


class MozartInterpreter:
    def __init__(self):
        self.evaluation_mapper = {
            ASTNodeType.IF.name: self.__evaluate_if,
            ASTNodeType.LOOP.name: self.__evaluate_loop,
            ASTNodeType.COMMAND.name: self.__evaluate_command,
            ASTNodeType.REGISTER.name: self.__evaluate_register,
            ASTNodeType.VARIABLE_ATTRIBUTION.name: self.__evaluate_variable_attribution,
            ASTNodeType.VARIABLE_DECLARATION.name: self.__evaluate_variable_declaration,
            ASTNodeType.ARITHMETIC_EXPRESSION.name: self.__evaluate_arithmetic_expression,
            ASTNodeType.ARITHMETIC_LITERAL.name: self.__evaluate_arithmetic_literal,
            ASTNodeType.ARITHMETIC_OPERATOR.name: self.__evaluate_arithmetic_operator,
            ASTNodeType.BINARY_LOGIC_OPERATOR.name: self.__evaluate_binary_logic_operator,
            ASTNodeType.BUILTIN_FUNCTIONS.name: self.__evaluate_builtin_functions,
            ASTNodeType.CHORD.name: self.__evaluate_chord,
            ASTNodeType.CHORD_LIST.name: self.__evaluate_chord_list,
            ASTNodeType.COMPARATIVE_OPERATOR.name: self.__evaluate_comparative_operator,
            ASTNodeType.EXPRESSION.name: self.__evaluate_expression,
            ASTNodeType.HARMONIC_FIELD.name: self.__evaluate_harmonic_field,
            ASTNodeType.IFELSE.name: self.__evaluate_ifelse,
            ASTNodeType.LITERAL.name: self.__evaluate_literal,
            ASTNodeType.LOGIC_EXPRESSION.name: self.__evaluate_logic_expression,
            ASTNodeType.MUSIC.name: self.__evaluate_music,
            ASTNodeType.NOTE.name: self.__evaluate_note,
            ASTNodeType.NOTE_LIST.name: self.__evaluate_note_list,
            ASTNodeType.PARAMS_LIST.name: self.__evaluate_params_list,
            ASTNodeType.SCALE.name: self.__evaluate_scale,
            ASTNodeType.INTEGER_LIST.name: self.__evaluate_integer_list,
            ASTNodeType.UNARY_LOGIC_OPERATOR.name: self.__evaluate_unary_logic_operator,
        }

        self.arithmetic_operation = {
            "+": self.sum,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
            "%": self.modulos
        }

        self.logic_operations = {
            "!": self.mozart_not,
            "&&": self.mozart_and,
            "||": self.mozart_or
        }

        self.comparative_operations = {
            ">": self.gt,
            "<": self.lt,
            ">=": self.ge,
            "<=": self.le,
            "==": self.et,
            "!=": self.ne
        }

        self.mozart_builtin_functions_mapper = {
            "belong": mozart_builtin_functions.belong,
            "transpose": mozart_builtin_functions.transpose,
            "get": mozart_builtin_functions.get,
            "append_note": mozart_builtin_functions.append_note,
            "append_chord": mozart_builtin_functions.append_chord
        }

    def run(self, code: str):
        # Syntax Analysis and Build AST
        ast = mozart_parser.parse(code)
        # Semantic Analysis and Interpretation
        return self.__interpret_ast(ast)

    @staticmethod
    def mozart_not(value: bool):
        return not value

    @staticmethod
    def mozart_and(a, b):
        return a and b

    @staticmethod
    def mozart_or(a, b):
        return a or b

    @staticmethod
    def gt(a, b):
        return a > b

    @staticmethod
    def lt(a, b):
        return a < b

    @staticmethod
    def ge(a, b):
        return a >= b

    @staticmethod
    def le(a, b):
        return a <= b

    @staticmethod
    def et(a, b):
        return a == b

    @staticmethod
    def ne(a, b):
        return a != b

    @staticmethod
    def sum(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError

        return a / b

    @staticmethod
    def modulos(a, b):
        if b == 0:
            raise ModuloZero

        return a % b

    def __interpret_ast(self, ast):
        program_state = {}
        return self.__evaluate_command(ast.root, program_state)

    def __evaluate_command(self, node: ASTNode, program_state):
        if len(node.children) == 2:
            program_state = self.__evaluate_command(node.children[0], program_state)
            program_state = self.__evaluate_command(node.children[1], program_state)
        else:
            program_state = self.evaluation_mapper[node.children[0].type.name](node.children[0], program_state)
        return program_state

    def __evaluate_if(self, node: ASTNode, program_state):
        # First child is the logic expression and the second is the command
        if self.__evaluate_logic_expression(node.children[0], program_state):
            program_state = self.__evaluate_command(node.children[1], program_state)

        return program_state

    def __evaluate_loop(self, node: ASTNode, program_state):
        # First child is the logic expression and the second is the command
        while self.__evaluate_logic_expression(node.children[0], program_state)[1]:
            program_state = self.__evaluate_command(node.children[1], program_state)

        return program_state

    def __evaluate_register(self, node: ASTNode, program_state):
        # first child is a expression
        value_type, music = self.__evaluate_expression(node.children[0], program_state)
        fp = open("./generated_music.mus", "w", encoding="utf-8")
        fp.write(str(music))
        fp.close()
        return program_state

    def __evaluate_variable_attribution(self, node: ASTNode, program_state):
        # first child is an expression, first value is the variable identifier
        value_type, value = self.__evaluate_expression(node.children[0], program_state)
        if node.value in program_state:
            if value_type == program_state[node.value][0]:
                program_state[node.value] = (value_type, value)
            else:
                raise WrongDomainVariableAttribution(value_type, program_state[node.value][0])
        else:
            raise NotExistentVariableAttribution(node.value)
        return program_state

    def __evaluate_variable_declaration(self, node: ASTNode, program_state):
        # first child is an expression
        # first value is the variable type
        # second value is the variable identifier
        value = self.__evaluate_expression(node.children[0], program_state)
        if not (node.value[1] in program_state):
            if value[0] == node.value[0]:
                program_state[node.value[1]] = (value[0], value[1])
            else:
                raise WrongDomainVariableAttribution(value[0], node.value[0])
        else:
            raise IdentifierAlreadyDefined(node.value[1])
        return program_state

    def __evaluate_arithmetic_expression(self, node: ASTNode, program_state):
        defined_operation_domains = [ValueType.INTEGER, ValueType.REAL]
        if len(node.children) == 0:
            return program_state[node.value]

        if len(node.children) == 3:
            value_type_a, value_a = self.__evaluate_arithmetic_expression(node.children[0], program_state)
            operator = self.__evaluate_arithmetic_operator(node.children[1], program_state)
            value_type_b, value_b = self.__evaluate_arithmetic_expression(node.children[2], program_state)

            if value_type_a != value_type_b:
                raise OperationBetweenDifferentDomain(value_type_a, value_type_b)

            if not (value_type_a in defined_operation_domains):
                raise WrongDomainOperation(value_type_a, defined_operation_domains)

            return value_type_a, self.arithmetic_operation[operator](value_a, value_b)

        if len(node.children) == 1:
            if node.children[0].type == ASTNodeType.ARITHMETIC_LITERAL:
                value_type, value = self.__evaluate_arithmetic_literal(node.children[0], program_state)
                return value_type, value

            if node.children[0].type == ASTNodeType.ARITHMETIC_EXPRESSION:
                value_type, value = self.__evaluate_arithmetic_expression(node.children[0], program_state)
                return value_type, value

    @staticmethod
    def __evaluate_arithmetic_literal(node: ASTNode, program_state):
        return node.value_type, node.value

    @staticmethod
    def __evaluate_arithmetic_operator(node: ASTNode, program_state):
        return node.value

    @staticmethod
    def __evaluate_binary_logic_operator(node: ASTNode, program_state):
        return node.value

    def __evaluate_builtin_functions(self, node: ASTNode, program_state):
        # First child is the params list and the value is the predefined_identifier
        params = self.__evaluate_params_list(node.children[0], program_state)
        value = self.mozart_builtin_functions_mapper[node.value](params, program_state)
        return value

    @staticmethod
    def __evaluate_chord(node: ASTNode, program_state):
        return ValueType.CHORD, node.value

    def __evaluate_chord_list(self, node: ASTNode, program_state):
        chord_list = []
        for chord in node.value:
            chord_list.append(self.__evaluate_chord(chord, program_state))
        return ValueType.CHORD_LIST, chord_list

    @staticmethod
    def __evaluate_comparative_operator(node: ASTNode, program_state):
        return node.value

    def __evaluate_expression(self, node: ASTNode, program_state):
        return self.evaluation_mapper[node.children[0].type.name](node.children[0], program_state)

    def __evaluate_harmonic_field(self, node: ASTNode, program_state):
        chord_list = self.__evaluate_chord_list(node.children[0], program_state)
        return ValueType.HARMONIC_FIELD, chord_list[1]

    def __evaluate_ifelse(self, node: ASTNode, program_state):
        # First child is the logic expression and the second is the command
        if self.__evaluate_logic_expression(node.children[0], program_state):
            program_state = self.__evaluate_command(node.children[1], program_state)
        else:
            program_state = self.__evaluate_command(node.children[2], program_state)

        return program_state

    def __evaluate_literal(self, node: ASTNode, program_state):
        if len(node.children) == 0:
            return node.value_type, node.value
        else:
            return self.evaluation_mapper[node.children[0].type.name](node.children[0], program_state)

    @staticmethod
    def __evaluate_unary_logic_operator(node: ASTNode, program_state):
        return node.value

    @staticmethod
    def __evaluate_note(node: ASTNode, program_state):
        return ValueType.NOTE, node.value

    @staticmethod
    def __evaluate_note_list(node: ASTNode, program_state):
        return ValueType.NOTE_LIST, node.value

    def __evaluate_scale(self, node: ASTNode, program_state):
        value_type, value = self.__evaluate_integer_list(node.children[0], program_state)
        return ValueType.SCALE, value

    @staticmethod
    def __evaluate_integer_list(node: ASTNode, program_state):
        return ValueType.INTEGER_LIST, node.value

    def __evaluate_music(self, node: ASTNode, program_state):
        note_list = self.__evaluate_note_list(node.value[0], program_state)
        return ValueType.MUSIC, (note_list, node.value[1])

    def __evaluate_params_list(self, node: ASTNode, program_state):
        params_list = []
        for param in node.value:
            params_list.append(self.__evaluate_expression(param, program_state))
        return params_list

    def __evaluate_logic_expression(self, node: ASTNode, program_state):
        if len(node.children) == 0:
            if node.value_type == ValueType.BOOLEAN:
                return ValueType.BOOLEAN, node.value

            if node.value_type == ValueType.IDENTIFIER:
                return program_state(node.value)

        if len(node.children) == 1:
            return self.__evaluate_logic_expression(node.children[0], program_state)

        if len(node.children) == 2:
            return self.logic_operations[node.value[0]](node.value[2])

        if len(node.children) == 3:
            if node.children[0].type == ASTNodeType.ARITHMETIC_EXPRESSION:
                value_type_a, value_a = self.__evaluate_arithmetic_expression(node.children[0], program_state)
                operator = self.__evaluate_comparative_operator(node.children[1], program_state)
                value_type_b, value_b = self.__evaluate_arithmetic_expression(node.children[2], program_state)
                return ValueType.BOOLEAN, self.comparative_operations[operator](value_a, value_b)

            if node.children[0].type == ASTNodeType.LOGIC_EXPRESSION:
                value_type_a, value_a = self.__evaluate_logic_expression(node.children[0], program_state)
                operator = self.__evaluate_binary_logic_operator(node.children[1], program_state)
                value_type_b, value_b = self.__evaluate_logic_expression(node.children[2], program_state)
                return value_type_a, self.logic_operations[operator](value_a, value_b)
