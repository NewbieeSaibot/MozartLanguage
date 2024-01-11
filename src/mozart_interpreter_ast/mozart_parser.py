from ply import yacc
from mozart_ast import AST, ASTNode, ASTNodeType, ValueType
import mozart_lex


syntax_error = False
tokens = mozart_lex.tokens


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
start = "program"


def p_program(p):
    'program : "{" command "}"'
    p[0] = AST(root=p[2])


# Command definitions
def p_command_command_command(p):
    r'command : command command'
    p[0] = ASTNode(type=ASTNodeType.COMMAND, children=[p[1], p[2]])


def p_command_loop(p):
    r'command : loop'
    p[0] = ASTNode(type=ASTNodeType.COMMAND, children=[p[1]])


def p_command_if_conditional(p):
    r'command : if_conditional'
    p[0] = ASTNode(type=ASTNodeType.COMMAND, children=[p[1]])


def p_command_if_else_conditional(p):
    r'command : if_else_conditional'
    p[0] = ASTNode(type=ASTNodeType.COMMAND, children=[p[1]])


def p_command_variable_attribution(p):
    r'command : variable_attribution END'
    p[0] = ASTNode(type=ASTNodeType.COMMAND, children=[p[1]])


def p_command_variable_declaration(p):
    r'command : variable_declaration END'
    p[0] = ASTNode(type=ASTNodeType.COMMAND, children=[p[1]])


def p_command_register(p):
    r'command : register_command END'
    p[0] = ASTNode(type=ASTNodeType.COMMAND, children=[p[1]])


def p_loop(p):
    r'loop : WHILE "(" logic_expression ")" "{" command "}"'
    p[0] = ASTNode(type=ASTNodeType.LOOP, children=[p[3], p[6]])


def p_if_conditional(p):
    r'if_conditional : IF "(" logic_expression ")" "{" command "}"'
    p[0] = ASTNode(type=ASTNodeType.IF, children=[p[3], p[6]])


def p_if_else_conditional(p):
    r'if_else_conditional : IF "(" logic_expression ")" "{" command "}" ELSE "{" command "}"'
    p[0] = ASTNode(type=ASTNodeType.IFELSE, children=[p[3], p[6], p[10]])


def p_register_command(p):
    r'register_command : REGISTER "(" expression ")"'
    p[0] = ASTNode(ASTNodeType.REGISTER, children=[p[3]])


def p_error(p):
    global syntax_error
    syntax_error = True


# Operators
def p_arithmetic_operator(p):
    '''arithmetic_operator : PLUS
                           | MINUS
                           | TIMES
                           | DIVISION
                           | MODULO'''
    p[0] = ASTNode(type=ASTNodeType.ARITHMETIC_OPERATOR, children=[], value=p[1])


def p_binary_logic_operator(p):
    '''binary_logic_operator : AND
                             | OR'''
    p[0] = ASTNode(ASTNodeType.BINARY_LOGIC_OPERATOR, [], value=p[1])


def p_unary_logic_operator(p):
    '''unary_logic_operator : NOT'''
    p[0] = ASTNode(ASTNodeType.UNARY_LOGIC_OPERATOR, [], value=p[1])


def p_comparative_operator(p):
    '''comparative_operator : GT
                            | LT
                            | GE
                            | LE
                            | EQUAL
                            | NOT_EQUAL'''
    p[0] = ASTNode(ASTNodeType.COMPARATIVE_OPERATOR, [], value=p[1])


# Builtin types
def p_NOTE(p):
    r'note : "(" REAL COMMA REAL COMMA INTEGER ")"'
    p[0] = ASTNode(ASTNodeType.NOTE, [], value=(p[2], p[4], p[6]))


def p_INTEGER_LIST(p):
    '''integer_list : INTEGER
                    | integer_list COMMA INTEGER'''
    if len(p) == 2:
        p[0] = ASTNode(ASTNodeType.INTEGER_LIST, [], value=[p[1]])
    else:
        p[1].value.append(p[3])
        p[0] = p[1]


def p_SCALE(p):
    r'scale : "[" integer_list "]"'
    p[0] = ASTNode(ASTNodeType.SCALE, children=[p[2]])


def p_CHORD(p):
    r'chord : "(" INTEGER COMMA INTEGER COMMA INTEGER ")"'
    p[0] = ASTNode(ASTNodeType.CHORD, children=[], value=(p[2], p[4], [6]))


def p_chord_list(p):
    '''chord_list : chord
                  | chord_list COMMA chord'''
    if len(p) == 2:
        p[0] = ASTNode(ASTNodeType.CHORD_LIST, children=[], value=[p[1]])
    else:
        p[1].value.append(p[3])
        p[0] = p[1]


def p_harmonic_field(p):
    r'harmonic_field : "[" chord_list "]"'
    p[0] = ASTNode(ASTNodeType.HARMONIC_FIELD, children=[p[2]])


def p_note_list(p):
    '''note_list : note
                 | note_list COMMA note'''
    if len(p) == 2:
        p[0] = ASTNode(ASTNodeType.NOTE_LIST, children=[], value=[p[1]])
    else:
        p[1].value.append(p[3])
        p[0] = p[1]


def p_music(p):
    '''music : "(" "[" note_list "]" COMMA REAL ")"
             | "(" "[" "]" COMMA REAL ")" '''
    if len(p) == 8:
        p[0] = ASTNode(ASTNodeType.MUSIC, children=[], value=(p[3], p[6]))
    if len(p) == 7:
        p[0] = ASTNode(ASTNodeType.MUSIC, children=[], value=(ASTNode(ASTNodeType.NOTE_LIST, children=[],
                                                                      value=[], value_type=ValueType.NOTE_LIST), p[5]))


# Commands
def p_variable_attribution(p):
    r'variable_attribution : IDENTIFIER "=" expression'
    p[0] = ASTNode(ASTNodeType.VARIABLE_ATTRIBUTION, children=[p[3]], value=p[1])


# More general rules
def p_variable_declaration(p):
    r'variable_declaration : VARIABLE_TYPE IDENTIFIER "=" expression'
    p[0] = ASTNode(ASTNodeType.VARIABLE_DECLARATION, children=[p[4]], value=(p[1], p[2]))


def p_literal_not_primitive(p):
    '''literal : note
               | scale
               | chord
               | harmonic_field
               | music'''
    p[0] = ASTNode(ASTNodeType.LITERAL, children=[p[1]])


def p_literal_primitive(p):
    '''literal : INTEGER
               | REAL
               | BOOLEAN
               '''
    p[0] = ASTNode(ASTNodeType.LITERAL, children=[], value=p[1])


def p_expression(p):
    '''expression : arithmetic_expression
                  | logic_expression
                  | literal
                  | builtin_functions'''
    p[0] = ASTNode(ASTNodeType.EXPRESSION, children=[p[1]])


def aux_get(p):
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


def p_builtin_functions(p):
    r'builtin_functions : PREDEFINED_IDENTIFIER "(" params_list ")"'
    p[0] = ASTNode(ASTNodeType.BUILTIN_FUNCTIONS, children=[p[3]], value=p[1])


def p_params_list(p):
    '''params_list : expression
                   | params_list COMMA expression'''
    if len(p) == 2:
        p[0] = ASTNode(ASTNodeType.PARAMS_LIST, children=[], value=[p[1]])
    else:
        p[1].value.append(p[3])
        p[0] = p[1]


def p_arithmetic_expression_value(p):
    r'arithmetic_expression : IDENTIFIER'
    p[0] = ASTNode(ASTNodeType.ARITHMETIC_EXPRESSION, children=[], value=p[1], value_type=ValueType.IDENTIFIER)


def p_arithmetic_expression_identifier(p):
    r'arithmetic_expression : arithmetic_literal'
    p[0] = ASTNode(ASTNodeType.ARITHMETIC_EXPRESSION, children=[p[1]])


def p_arithmetic_expression_in_brackets(p):
    r'arithmetic_expression : "(" arithmetic_expression ")"'
    p[0] = ASTNode(ASTNodeType.ARITHMETIC_EXPRESSION, children=[p[2]])


def p_arithmetic_expression_operation(p):
    r'arithmetic_expression : arithmetic_expression arithmetic_operator arithmetic_expression'
    p[0] = ASTNode(ASTNodeType.ARITHMETIC_EXPRESSION, children=[p[1], p[2], p[3]])


def p_logic_expression_boolean(p):
    r'logic_expression : BOOLEAN'
    p[0] = ASTNode(ASTNodeType.LOGIC_EXPRESSION, children=[], value_type=ValueType.BOOLEAN, value=p[1])


def p_logic_expression_identifier(p):
    r'logic_expression : IDENTIFIER'
    p[0] = ASTNode(ASTNodeType.LOGIC_EXPRESSION, children=[], value_type=ValueType.IDENTIFIER, value=p[1])


def p_logic_expression_in_brackets(p):
    r'logic_expression : "(" logic_expression ")"'
    p[0] = ASTNode(ASTNodeType.LOGIC_EXPRESSION, children=[p[2]])


def p_logic_expression_ae_co_ae(p):
    r'logic_expression : "(" arithmetic_expression comparative_operator arithmetic_expression ")"'
    p[0] = ASTNode(ASTNodeType.LOGIC_EXPRESSION, children=[p[2], p[3], p[4]])


def p_logic_expression_le_lo_le(p):
    r'logic_expression : logic_expression binary_logic_operator logic_expression'
    p[0] = ASTNode(ASTNodeType.LOGIC_EXPRESSION, children=[p[1], p[2], p[3]])


def p_logic_expression_uo_le(p):
    r'logic_expression : unary_logic_operator logic_expression'
    p[0] = ASTNode(ASTNodeType.LOGIC_EXPRESSION, children=[p[1], p[2]])


def p_arithmetic_literal_real(p):
    r'arithmetic_literal : REAL'
    p[0] = ASTNode(ASTNodeType.ARITHMETIC_LITERAL, children=[], value_type=ValueType.REAL, value=p[1])


def p_arithmetic_literal_integer(p):
    r'arithmetic_literal : INTEGER'
    p[0] = ASTNode(ASTNodeType.ARITHMETIC_LITERAL, children=[], value_type=ValueType.INTEGER, value=p[1])


# Productions
mozart_parser = yacc.yacc()


def parse(data, debug=0):
    p = mozart_parser.parse(data, debug=debug)
    if syntax_error:
        raise SyntaxError("Solve the syntax of your code!")
    return p
