import ply.yacc as yacc
import ply.lex as lex
from pickle import dump

literals = ["=", "(", ")", "{", "}", "[", "]"]

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
    "IDENTIFIER",
    "PREDEFINED_IDENTIFIER",
    "VARIABLE_TYPE",
    "END",
    "COMMA")

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

t_IF = r'if'
t_ELSE = r'else'


# Predefined Types
def t_BOOLEAN(t):
    r'(True|False)'
    if str(t.value) == "True":
        t.value = ('boolean', True)
    else:
        t.value = ('boolean', False)
    return t


def t_REAL(t):
    '-?[1-9][0-9]*.[0-9]+'
    t.value = ("real", float(t.value))
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
        t.value = ("integer", pitch_value)
    else:
        t.value = ("integer", int(t.value))
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
    return t


t_COMMA = r','
t_END = r';'
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

# Tokens


# Build the lexer
lexer = lex.lex()

# Define program state
program_state = {}

# Define precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVISION'),
    ('left', 'COMMA')
)


# Aux functions
def domain_checker(variable_type: str, value_type: str):
    return variable_type == value_type


# Parsing rules
start = "start"


# Start
def p_program_start(p):
    r'start : scope'
    p[0] = p[1]


def p_scope(p):
    r'scope : "{" command "}"'
    p[0] = p[2]


def p_command(p):
    '''command : variable_declaration END
               | variable_attribution END
               | command command
               | register_command
               | conditional
               '''
    if len(p) == 3:
        if type(p[1]) == str:
            if str(p[1]).startswith("[ERROR]"):
                p[0] = p[1]
        elif type(p[2]) == str:
            if str(p[2]).startswith("[ERROR]"):
                p[0] = p[2]
        else:
            p[0] = "Commands Executed"
    elif len(p) == 2:
        p[0] = p[1]


def p_conditional(p):
    '''conditional : IF "(" logic_expression ")" scope ELSE scope'''
    p[0] = ""

    # implementar iterativamente linha a linha o interpretador


def p_register_command(p):
    r'register_command : REGISTER "(" expression ")"'
    if type(p[3]) == str:
        if str(p[3]).startswith("[ERROR]"):
            p[0] = p[3]
    elif len(p[3]) == 2:
        if p[3][0] == "music":
            p[0] = "Command Executed!"
            fp = open("../../src/generated_music.pkl", "w", encoding="utf-8")
            dump(p[3][1], fp)
            fp.close()
        else:
            p[0] = f"[ERROR] Wrong domain! Variable type: music. Value from type: {p[3][0]}"
    else:
        p[0] = "[ERROR] Unidentified Error!"


def p_error(p):
    if p:
        print(f"Syntax error at {p.value}")
    else:
        print("Syntax error at EOF")


# Operators
def p_arithmetic_operator(p):
    '''arithmetic_operator : PLUS
                           | MINUS
                           | TIMES
                           | DIVISION
                           | MODULO'''
    p[0] = p[1]


def p_binary_logic_operator(p):
    '''binary_logic_operator : AND
                             | OR'''
    p[0] = p[1]


def p_unary_logic_operator(p):
    '''unary_logic_operator : NOT'''
    p[0] = p[1]


def p_comparative_operator(p):
    '''comparative_operator : GT
                            | LT
                            | GE
                            | LE
                            | EQUAL
                            | NOT_EQUAL'''
    p[0] = p[1]


def p_unary_operator(p):
    '''unary_operator : unary_logic_operator'''
    p[0] = p[1]


def p_binary_operator(p):
    '''binary_operator : arithmetic_operator
                       | comparative_operator
                       | binary_logic_operator'''
    p[0] = p[1]


# Builtin types
def p_NOTE(p):
    r'note : "(" REAL "," REAL "," INTEGER ")"'
    p[0] = ("note", (p[2], p[4], p[6]))


def p_INTEGER_LIST(p):
    '''integer_list : INTEGER
                    | integer_list COMMA INTEGER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_SCALE(p):
    r'scale : "[" integer_list "]"'
    p[0] = ("scale", p[2])


def p_CHORD(p):
    r'chord : "(" INTEGER COMMA INTEGER COMMA INTEGER ")"'
    p[0] = ("chord", (p[2], p[4], [6]))


def p_chord_list(p):
    '''chord_list : chord
                  | chord_list COMMA chord'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_harmonic_field(p):
    r'harmonic_field : "[" chord_list "]"'
    p[0] = ("harmonic_field", p[2])


def p_note_list(p):
    '''note_list : note
                 | note_list COMMA note'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_music(p):
    r'music : "(" note_list "," REAL ")"'
    p[0] = ('music', (p[2], p[4]))


# Commands
def p_variable_attribution(p):
    r'variable_attribution : IDENTIFIER "=" expression'

    if type(p[3]) == str:
        if str(p[3]).startswith("[ERROR]"):
            p[0] = p[3]

    if p[1] in program_state.keys():
        # To do
        # Check if attribution is from values in the same domain of variable type
        if domain_checker(program_state[p[1]][0], p[3][0]):
            program_state[p[1]] = p[3]
            p[0] = "Command Executed!"
        else:
            p[0] = f"[ERROR] Wrong domain! Variable type: {program_state[p[1]][0]}. Value from type: {p[3][0]}"
    else:
        p[0] = "[ERROR] Variable Not Defined!"


# More general rules
def p_variable_declaration(p):
    r'variable_declaration : VARIABLE_TYPE IDENTIFIER "=" expression'
    if type(p[4]) == str:
        p[0] = p[4]
    elif p[2] in program_state.keys():
        p[0] = "[ERROR] Variable Already Defined!"
    else:
        # To do
        # Check if attribution is from values in the same domain of variable type
        if domain_checker(p[1], p[4][0]):
            program_state[p[2]] = p[4]
            p[0] = "Command Executed!"
        else:
            p[0] = f"[ERROR] Wrong domain! Variable type: {p[1]}. Value from type: {p[4][0]}"


def p_literal(p):
    '''literal : INTEGER
               | REAL
               | BOOLEAN
               | note
               | scale
               | chord
               | harmonic_field
               | music'''
    p[0] = p[1]


def p_expression(p):
    '''expression : arithmetic_expression
                  | logic_expression
                  | literal'''
    p[0] = p[1]


def p_arithmetic_expression(p):
    '''arithmetic_expression : arithmetic_literal
                             | "(" arithmetic_expression ")"
                             | IDENTIFIER
                             | arithmetic_expression arithmetic_operator arithmetic_expression'''
    types = ["real", "integer"]
    # First Production
    if len(p) == 2:
        if p[1][0] in types:
            # arithmetic_literal
            p[0] = p[1]
        else:
            # IDENTIFIER
            if p[1] in program_state.keys():
                p[0] = program_state[p[1]]
            else:
                p[0] = "[ERROR] Variable Not Defined!"
    else:
        if p[1] == "(":
            # "(" arithmetic_expression ")"
            p[0] = p[2]
        else:
            # arithmetic_expression arithmetic_operator arithmetic_expression
            # check same domain
            if type(p[1]) == str:
                if str(p[1]).startswith("[ERROR]"):
                    p[0] = p[1]
            elif type(p[3]) == str:
                if str(p[3]).startswith("[ERROR]"):
                    p[0] = p[3]
            else:
                if p[1][0] == p[3][0]:
                    if p[2] == "+":
                        p[0] = (p[1][0], p[1][1] + p[3][1])
                    if p[2] == "-":
                        p[0] = (p[1][0], p[1][1] - p[3][1])
                    if p[2] == "*":
                        p[0] = (p[1][0], p[1][1] * p[3][1])
                    if p[2] == "/":
                        p[0] = (p[1][0], p[1][1] / p[3][1])
                    if p[2] == "%":
                        if p[1][0] == "integer":
                            p[0] = (p[1][0], p[1][1] % p[3][1])
                        else:
                            p[0] = "[ERROR] Operator % is only defined for integers!"
                else:
                    p[0] = f"[ERROR] Values from different types: {p[1][0]} and {p[3][0]}"


def p_logic_expression(p):
    '''logic_expression : BOOLEAN
                        | IDENTIFIER
                        | "(" logic_expression ")"
                        | "(" arithmetic_expression comparative_operator arithmetic_expression ")"
                        | logic_expression binary_logic_operator logic_expression
                        | unary_logic_operator logic_expression'''
    if len(p) == 2:
        if len(p[1]) == 2:
            # Identifier
            p[0] = p[1]
        else:
            # Boolean
            if p[1] in program_state.keys():
                p[0] = program_state[p[1]]
            else:
                p[0] = "[ERROR] Variable Not Defined!"
    elif len(p) == 3:
        # unary_logic_operator logic_expression
        if type(p[2]) == str:
            if str(p[2]).startswith("[ERROR]"):
                p[0] = p[2]
        else:
            p[0] = (p[2][0], not p[2][1])
    elif len(p) == 4:
        if p[1] == "(":
            # "(" logic_expression ")"
            p[0] = p[2]
        else:
            # logic_expression binary_operator logic_expression
            if type(p[1]) == str:
                # its an error
                if str(p[1]).startswith("[ERROR]"):
                    p[0] = p[1]
            elif type(p[3]) == str:
                # its an error
                if str(p[3]).startswith("[ERROR]"):
                    p[0] = p[3]
            else:
                if p[3] == "&&":
                    p[0] = (p[1][0], p[1][1] and p[3][1])
                if p[3] == "||":
                    p[0] = (p[1][0], p[1][1] or p[3][1])

        # other case
    elif len(p) == 6:
        # "(" arithmetic_expression comparative_operator arithmetic_expression ")"
        if type(p[2]) == str:
            # its an error
            if str(p[2]).startswith("[ERROR]"):
                p[0] = p[2]
        elif type(p[4]) == str:
            # its an error
            if str(p[4]).startswith("[ERROR]"):
                p[0] = p[4]
        else:
            if p[3] == ">":
                p[0] = ('boolean', p[2][1] > p[4][1])
            if p[3] == ">=":
                p[0] = ('boolean', p[2][1] >= p[4][1])
            if p[3] == "<":
                p[0] = ('boolean', p[2][1] < p[4][1])
            if p[3] == "<=":
                p[0] = ('boolean', p[2][1] <= p[4][1])
            if p[3] == "==":
                p[0] = ('boolean', p[2][1] == p[4][1])
            if p[3] == "!=":
                p[0] = ('boolean', p[2][1] != p[4][1])
    else:
        pass


def p_arithmetic_literal(p):
    '''arithmetic_literal : REAL
                          | INTEGER'''
    p[0] = p[1]


# Productions
parser = yacc.yacc()
# fp = open("./example_1.mozart", "r", encoding="utf-8")
# code = fp.read()
code = "{" \
       "boolean id = (( 3 % 3 ) == 1);" \
       "id = True;" \
       "harmonic_field campo = [(1, 2, 3), (2, 3, 4)];" \
       "register(3)" \
       "}"
print(yacc.parse(code))


lexer.input(code)
for token in lexer:
    print(token)

print(program_state)
