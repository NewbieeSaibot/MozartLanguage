from ply import *
import logging
logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)

contexto = 0

def get_contexto():
    return contexto


# Tabela de simbolos
# {ID {valor, tipo, contexto}}
simbolos = {}

# Palavras reservadas <palavra>:<TOKEN>
reserved = {
            'if': 'IF',
            'else': 'ELSE',
            'switch': 'SWITCH',
            'case': 'CASE',

            'while': 'WHILE',
            'for': 'FOR',
            'do': 'DO',

            'unsigned': 'UNSIGNED',
            'int': 'INT',
            'long': 'LONG',
            'short': 'SHORT',

            'float': 'FLOAT',
            'double': 'DOUBLE',

            'void': 'VOID',
            'struct': 'STRUCT',
            'typedef': 'TYPEDEF',
            'static': 'STATIC',

            'char': 'CHAR',

            'return': 'RETURN',
            'main': 'MAIN'
        }

# Demais TOKENS
tokens = [
            'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
            'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE', 'EE',
            'COMMA', 'SEMI', 'STRING', 'INTEGER', 'FLOATING',
            'ID', 'NEWLINE', 'SEMICOLON', 'RBRACE', 'LBRACE'
        ] + list(reserved.values())

t_ignore = ' \t\n'


def t_REM(t):
    r'REM .*'
    return t


# Definição de Identificador com expressão regular r'<expressão>'
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RBRACE = r'\}'
t_LBRACE = r'\{'
t_SEMICOLON = r'\;'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='
t_EE = r'=='
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOATING = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


# Constroi o analisador léxico
lexer = lex.lex()


# Definições da gramática
def p_inicio(p):
    'inicio : INT MAIN LPAREN tipo RPAREN blocoprincipal'
    print("reconheci bloco inicial")


def p_blocoprincipal(p):
    'blocoprincipal : abre_escopo declaracoes fecha_escopo'
    print("reconheci bloco principal")


def p_declaracoes(p):
    '''declaracoes : declaracao_variavel
                    | atribuicao
                    | atribuicao declaracoes
                    | condicional
                    | condicional declaracoes
                    | estrutura_de_repeticao
                    | estrutura_de_repeticao declaracoes'''

    print("Reconheci p_declaracoes")


def p_declaracao_variavel(p):
    '''declaracao_variavel : tipo ID SEMICOLON
                           | tipo ID SEMICOLON declaracoes
                           | tipo ID comma_declaration SEMICOLON
                           | declaracao_com_atribuicao'''

    print("Reconheci declaracoes sem atribuicao")

    if len(p) > 2:
        if p[2] in list(simbolos.keys()):
            print("Variável com mesmo ID já declarada anteriormente!")
        else:
            simbolos[p[2]] = {'valor': None, 'tipo': p[1], 'contexto': get_contexto()}


def p_declaracao_com_atribuicao(p):
    '''declaracao_com_atribuicao : tipo ID EQUALS expressao SEMICOLON
                                 | tipo ID EQUALS expressao SEMICOLON declaracoes'''

    print("Reconheci declaracoes com atribuicao")

    if p[2] in list(simbolos.keys()):
        print("Variável com mesmo ID já declarada anteriormente!")
    else:
        simbolos[p[2]] = {'valor': p[4], 'tipo': p[1], 'contexto': get_contexto()}


def p_atribuicao(p):
    'atribuicao : ID EQUALS valor SEMICOLON'

    print("Reconheci atribuicao")

    if p[1] in list(simbolos.keys()):
        simbolos[p[1]]['valor'] = p[3]
    else:
        print("Atribuição de variável não declarada")

    p[0] = p[1]


def p_comma_declaration(p):
    '''comma_declaration : COMMA ID
                        | COMMA ID comma_declaration'''

    print("Reconheci declaracoes multiplas")

    if p[2] in list(simbolos.keys()):
        print("Variável com mesmo ID já declarada anteriormente!")
    else:
        simbolos[p[2]] = {'valor': None, 'tipo': None, 'contexto': get_contexto()}

#Gerenciamento de níveis de contexto
def p_abre_escopo(p):
    'abre_escopo : LBRACE'
    global contexto
    contexto = get_contexto() + 1


def p_fecha_escopo(p):
    'fecha_escopo : RBRACE'
    global contexto
    contexto = get_contexto() - 1


def p_estrutura_de_repeticao(p):
    '''estrutura_de_repeticao : FOR LPAREN ID EQUALS expressao SEMICOLON ID comparator expressao SEMICOLON ID EQUALS expressao RPAREN abre_escopo declaracoes fecha_escopo
                              | WHILE LPAREN expressao RPAREN abre_escopo declaracoes fecha_escopo'''

    print("Reconheci p_estrutura_de_repeticao")


def p_condicional(p):
    '''condicional : IF LPAREN expressao RPAREN abre_escopo declaracoes fecha_escopo
                    | IF LPAREN expressao RPAREN abre_escopo declaracoes fecha_escopo ELSE abre_escopo declaracoes fecha_escopo
                    | IF LPAREN expressao RPAREN abre_escopo declaracoes fecha_escopo outro_condicional
                    | IF LPAREN expressao RPAREN abre_escopo declaracoes fecha_escopo outro_condicional ELSE abre_escopo declaracoes fecha_escopo '''
    print("Reconheci p_condicional")



def p_outro_condicional(p):
    '''outro_condicional : ELSE IF LPAREN expressao RPAREN abre_escopo declaracoes fecha_escopo
                        | ELSE IF LPAREN expressao RPAREN abre_escopo declaracoes fecha_escopo outro_condicional'''


def p_expressao(p):
    '''expressao : valor
                  | LPAREN expressao RPAREN
                  | ID
                  | expressao operador_binario expressao
                  | expressao comparator expressao
                  | MINUS expressao'''

    print("Reconheci comparador de expressoes")
    p[0] = p[1]


def p_comparator(p):
    '''comparator : LT
                  | LE
                  | GT
                  | GE
                  | NE'''


def p_operador_binario(p):
    '''operador_binario : PLUS
                         | MINUS
                         | TIMES
                         | POWER
                         | DIVIDE'''


def p_valor(p):
    '''valor : INTEGER
              | FLOATING
              | STRING'''
    p[0] = p[1]


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | VOID'''


import ply.yacc as yacc
yacc.yacc()

# entrada do arquivo
file = open("./test_data/final_test.c", 'r')
data = file.read()

# string de teste como entrada do analisador léxico
lexer.input(data)

# Tokenização
for tok in lexer:
     print(tok)

yacc.parse(data, debug=logging.getLogger())
print(simbolos)
