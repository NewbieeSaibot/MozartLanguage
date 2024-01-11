from ply import *
from mozart_ast import ValueType

literals = ["=", "(", ")", "[", "]", "{", "}"]

tokens = (
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVISION",
    "MODULO",
    "AND",
    "OR",
    "NOT",
    "GT",
    "LT",
    "GE",
    "LE",
    "EQUAL",
    "NOT_EQUAL",
    "BOOLEAN",
    "REAL",
    "IF",
    "ELSE",
    "INTEGER",
    "REGISTER",
    "VARIABLE_TYPE",
    "IDENTIFIER",
    "PREDEFINED_IDENTIFIER",
    "END",
    "COMMA",
    "WHILE")

# Operators
# Arithmetic Operators
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'

# Logic Operators
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# Comparators
t_GT = r">"
t_LT = r"<"
t_GE = r">="
t_LE = r"<="
t_EQUAL = r"=="
t_NOT_EQUAL = r"!="
# End Operators


def t_IF(t):
    r'if'
    return t


def t_ELSE(t):
    r'else'
    return t


def t_WHILE(t):
    r'while'
    return t


# Predefined Types
def t_BOOLEAN(t):
    r'(True|False)'
    if str(t.value) == "True":
        t.value = (ValueType.BOOLEAN, True)
    else:
        t.value = (ValueType.BOOLEAN, False)
    return t


def t_REAL(t):
    '-?[1-9][0-9]*.[0-9]+'
    t.value = (ValueType.REAL, float(t.value))
    return t


def t_INTEGER(t):
    r'(\-?0|\-?[1-9][0-9]*)|[A-G]\#?[0-9]'
    pitch_to_int = {
        "G": 10,
        "A": 12,
        "B": 14,
        "C": 3,
        "D": 5,
        "E": 7,
        "F": 8
    }
    pitch_value = 0
    if str(t.value)[0].isalpha():
        pitch_value += pitch_to_int[str(t.value)[0]]
        if len(str(t.value)) == 3:
            pitch_value += 1

        pitch_value += int(str(t.value)[-1]) * 12
        t.value = (ValueType.INTEGER, pitch_value)
    else:
        t.value = (ValueType.INTEGER, int(t.value))
    return t


def t_PREDEFINED_IDENTIFIER(t):
    r'(belong|transpose|get|append_note|append_chord)'
    return t


def t_VARIABLE_TYPE(t):
    r'(boolean|integer|real|note|scale|chord|harmonic_field|music)'
    return t


def t_REGISTER(t):
    r'register'
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z]+'
    #r'[a-zA-Z]+'
    #$|^(?!(?:apple|banana|cherry)$)'
    return t


t_COMMA = r','
t_END = r';'
t_ignore = ' \t\n'


# Error handling rule
def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
