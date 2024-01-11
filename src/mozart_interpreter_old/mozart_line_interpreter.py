import ply.yacc as yacc
import ply.lex as lex

literals = ["=", "(", ")", "[", "]"]

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
    "OPEN_SCOPE",
    "END_SCOPE",
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


def t_END_SCOPE(t):
    r'}'
    t.value = "END_SCOPE"
    return t


def t_OPEN_SCOPE(t):
    r'{'
    t.value = "OPEN_SCOPE"
    return t


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
start = "command"


# Start
def p_command(p):
    '''command : variable_declaration END
               | variable_attribution END
               | command command END
               | register_command END
               | if_conditional
               | else_conditional
               | OPEN_SCOPE
               | END_SCOPE
               | loop
               '''

    if len(p) == 3:
        if type(p[1]) == str:
            p[0] = p[1]
        elif type(p[2]) == str:
            p[0] = p[2]
        else:
            p[0] = "Commands Executed"
    elif len(p) == 2:
        p[0] = p[1]


def p_loop(p):
    r'loop : WHILE "(" logic_expression ")" OPEN_SCOPE'
    p[0] = ("while", p[3][1])


def p_if_conditional(p):
    r'if_conditional : IF "(" logic_expression ")" OPEN_SCOPE'
    p[0] = ("if", p[3][1])
    # implementar iterativamente linha a linha o interpretador


def p_else_conditional(p):
    r'else_conditional : END_SCOPE ELSE OPEN_SCOPE'
    p[0] = ("else", 0)
    # implementar iterativamente linha a linha o interpretador


def p_register_command(p):
    r'register_command : REGISTER "(" expression ")"'
    if type(p[3]) == str:
        if str(p[3]).startswith("[ERROR]"):
            p[0] = p[3]
    elif len(p[3]) == 2:
        if p[3][0] == "music":
            p[0] = "Command Executed!"
            fp = open("generated_music.mus", "w", encoding="utf-8")
            fp.write(str(p[3][1]))
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
    r'note : "(" REAL COMMA REAL COMMA INTEGER ")"'
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
    '''music : "(" "[" note_list "]" COMMA REAL ")"
             | "(" "[" "]" COMMA REAL ")" '''
    if len(p) == 8:
        p[0] = ('music', (p[3], p[6]))
    if len(p) == 7:
        p[0] = ('music', ([], p[5]))


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
                  | literal
                  | builtin_functions'''
    p[0] = p[1]


def p_builtin_functions(p):
    r'builtin_functions : PREDEFINED_IDENTIFIER "(" params_list ")"'
    if p[1] == "get":
        get_types = ["chord", "scale", "harmonic_field"]
        if len(p[3]) == 2:
            if p[3][0][0] in get_types:
                if p[3][1][0] == 'integer':
                    p[0] = p[3][0][1][p[3][1][1]]
                else:
                    p[0] = f"[ERROR] Position must be an integer! Got {p[3][1][0]}"
            else:
                p[0] = f"[ERROR] Expected one of the following types: {get_types}. Got {p[3][0][0]}"
        else:
            p[0] = f"[ERROR] Wrong number of params. Expected 2, got {len(p[3])}"
    else:
        p[0] = f"Function will be implemented in the next version!"


def p_params_list(p):
    '''params_list : expression
                   | params_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
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

fp = open("../../data/mozart_code_examples/example_1.mozart", "r", encoding="utf-8")
code_lines = fp.readlines()

stack = ["OPEN_SCOPE"]
# Interpretador
program_counter = 0
debug = False
while True:
    if code_lines[program_counter].strip() != "":
        out = yacc.parse(code_lines[program_counter])
        print("pc", program_counter + 1, "parser out:", out, "start_stack:", stack)
        if type(out) == tuple:
            if out[0] == "if" and out[1] == True:
                # if é verdadeiro -> segue normalmente o fluxo, pulando o bloco else
                stack.append("if_true")
            elif out[0] == "if" and out[1] == False:
                stack.append("if_false")
                # if é falso, pule ao bloco else e execute normalmente seguindo em frente
                # run lexer until find a END_SCOPE
                close_line = -1
                control_stack = ["OPEN_SCOPE"]
                for i in range(program_counter + 1, len(code_lines)):
                    lexer.input(code_lines[i])

                    for token in lexer:
                        if "OPEN_SCOPE" in str(token):
                            control_stack.append("OPEN_SCOPE")
                        if "END_SCOPE" in str(token):
                            control_stack.pop()

                        if len(control_stack) == 0:
                            close_line = i - 1
                            break
                    if close_line != -1:
                        break
                program_counter = close_line
            elif out[0] == "else":
                if len(stack) == 0:
                    print("[ERROR] Is this else necessary? The scope stack is empty!")
                if stack[-1] == "if_true":
                    # Então esse bloco de código deve ser pulado, pois o bloco a executar era do if
                    stack.pop()
                    close_line = -1
                    control_stack = ["OPEN_SCOPE"]
                    for i in range(program_counter + 1, len(code_lines)):
                        lexer.input(code_lines[i])
                        for token in lexer:
                            if "OPEN_SCOPE" in str(token):
                                control_stack.append("OPEN_SCOPE")
                            if "END_SCOPE" in str(token):
                                control_stack.pop()

                            if len(control_stack) == 0:
                                close_line = i
                                break
                        if close_line != -1:
                            break
                    program_counter = close_line
                elif stack[-1] == "if_false":
                    # o bloco deve ser executado normalmente, pois caiu no else
                    stack.pop()
            elif out[0] == "while":
                if out[1]:
                    # The condition is true, so run the loop normally
                    stack.append(("loop", program_counter - 1))
                else:
                    # The condition is false, so go to the end of the loop
                    close_line = -1
                    control_stack = ["OPEN_SCOPE"]
                    for i in range(program_counter + 1, len(code_lines)):
                        lexer.input(code_lines[i])

                        for token in lexer:
                            if "OPEN_SCOPE" in str(token):
                                control_stack.append("OPEN_SCOPE")
                            if "END_SCOPE" in str(token):
                                control_stack.pop()

                            if len(control_stack) == 0:
                                close_line = i
                                break
                        if close_line != -1:
                            break
                    program_counter = close_line
            else:
                print("Ih rapaz!")
        elif type(out) == str:
            if out == "END_SCOPE":
                if type(stack[-1]) == tuple:
                    if stack[-1][0] == "loop":
                        program_counter = stack[-1][1]
                        stack.pop()
                else:
                    stack.pop()
    program_counter += 1
    if program_counter == len(code_lines):
        break

    # Debug
    if debug:
        lexer.input(code_lines[program_counter])
        for token in lexer:
            print(token)

print("final state", program_state)
print("final stack", stack)
