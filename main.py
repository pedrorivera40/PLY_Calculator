# The following code correspond to a programming tutorial from http://www.dabeaz.com/ along with howCode YouTube channel.
# It consists on implementing a calculator app with Python's PLY library.

import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [

    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQUALS',
    'MODULO',
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_MODULO = r'\%'

t_ignore = r' '

def t_FLOAT(t):
    r'\d\.\d+' # FLOAT corresponds to an INT followed by '.' and a sequence of one or more consecutive integers...
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+' # INT corresponds to one or more consecutive occurrences an integer...
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_error(t):
    print("ILLEGAL CHARACTERS!")
    t.lexer.skip(1)

env = {}

def run(p):
    global env
    if type(p) == tuple :
        if p[0] == '+' : return run(p[1]) + run(p[2])
        elif p[0] == '-' : return run(p[1]) - run(p[2])
        elif p[0] == '*' : return run(p[1]) * run(p[2])
        elif p[0] == '/' : return run(p[1]) / run(p[2])
        elif p[0] == '%' : return run(p[1]) % run(p[2])
        elif p[0] == '=' :
            env[p[1]] = run(p[2])
            print(env[p[1]])
        elif p[0] == 'var' :
            if p[1] not in env : return "UNDECLARED VARIABLE!"
            return env[p[1]]
    else : return p


def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_expression_int_float(p):
    '''
    expression :  INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression(p):
    '''
    expression : expression MODULO expression
               | expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

def p_error(p):
    print("Syntax Error in: " + p.value)

lexer = lex.lex()

precedence = (('left', 'PLUS', 'MINUS'), ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'))

parser = yacc.yacc()

while True :

    try :
        line = input('> ')
    except EOFError : break
    parser.parse(line)

