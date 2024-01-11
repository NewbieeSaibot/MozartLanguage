from dataclasses import dataclass
from enum import Enum
from typing import Any, List


class ValueType(Enum):
    BOOLEAN = 0
    IDENTIFIER = 1
    REAL = 2
    INTEGER = 3
    CHORD = 4
    CHORD_LIST = 5
    HARMONIC_FIELD = 6
    NOTE = 7
    NOTE_LIST = 8
    SCALE = 9
    INTEGER_LIST = 10


class ASTNodeType(Enum):
    COMMAND = 0
    IF = 1
    LOOP = 2
    VARIABLE_ATTRIBUTION = 3
    VARIABLE_DECLARATION = 4
    REGISTER = 5
    IFELSE = 6
    ARITHMETIC_OPERATOR = 7
    BINARY_LOGIC_OPERATOR = 8
    NOTE = 9
    SCALE = 10
    CHORD = 11
    UNARY_LOGIC_OPERATOR = 12
    UNARY_OPERATOR = 13
    BINARY_OPERATOR = 14
    COMPARATIVE_OPERATOR = 15
    CHORD_LIST = 16
    HARMONIC_FIELD = 17
    NOTE_LIST = 18
    MUSIC = 19
    LITERAL = 20
    EXPRESSION = 21
    ARITHMETIC_EXPRESSION = 22
    LOGIC_EXPRESSION = 23
    BUILTIN_FUNCTIONS = 24
    PARAMS_LIST = 25
    ARITHMETIC_LITERAL = 26
    INTEGER_LIST = 27


@dataclass
class ASTNode:
    type: ASTNodeType
    children: List['ASTNode']
    value_type: ValueType = None
    value: Any = None


class AST:
    def __init__(self, root: ASTNode):
        self.root = root
