import re

import ply.lex as lex
import ply.yacc as yacc


MAX_COALITION = 0
# Token
tokens = (
    'LPAREN',
    'RPAREN',
    'AND',
    'OR',
    'NOT',
    'IMPLIES',
    'UNTIL',
    'GLOBALLY',
    'NEXT',
    'EVENTUALLY',
    'PROP',
    'COALITION'

)

# Espressioni regolari per i token
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AND = r'&&|\&|and'
t_OR = r'\|\||\||or'
t_NOT = r'!|not'
t_IMPLIES = r'->|>|implies'
t_PROP = r'[a-z]'
t_UNTIL = r'U|until'
t_GLOBALLY = r'G|globally|always'
t_NEXT = r'X|next'
t_EVENTUALLY = r'F|eventually'
t_COALITION = r'<\d+>'



# Gestione degli errori di token
def t_error(t):
    t.lexer.skip(1)


# Grammatica
def p_expression_binary(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | expression IMPLIES expression'''
    p[0] = (p[2], p[1], p[3])


class CoalitionValueError(Exception):
    pass

def p_expression_ternary(p):
    '''expression : COALITION expression UNTIL expression'''
    coalition_value = int(re.findall(r'\d+', p[1])[0])
    if coalition_value > int(MAX_COALITION):
        raise CoalitionValueError(f"Coalition value {coalition_value} exceeds maximum of {MAX_COALITION}")
    p[0] = (p[1] + p[3], p[2], p[4])


def p_expression_unary(p):
    '''expression : COALITION GLOBALLY expression
                  | COALITION NEXT expression
                  | COALITION EVENTUALLY expression'''
    coalition_value = int(re.findall(r'\d+', p[1])[0])
    if coalition_value > int(MAX_COALITION):
        raise CoalitionValueError(f"Coalition value {coalition_value} exceeds maximum of {MAX_COALITION}")
    p[0] = (p[1] + p[2], p[3])


def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = (p[1], p[2])


def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_expression_prop(p):
    '''expression : PROP'''
    p[0] = p[1]


def p_error(p):
   pass



# lexer e parser
lexer = lex.lex()
parser = yacc.yacc()


def do_parsing(formula, n_agent):
    global MAX_COALITION
    MAX_COALITION = n_agent
    try:
        result = parser.parse(formula)
        return result
    except SyntaxError:
        return None  # Restituisci un valore speciale se il parsing fallisce
    except CoalitionValueError as e:
        print("errore")
        return None
def get_lexer():
    return lexer

def verify(token_name, string):
    lexer.input(string)
    for token in lexer:
        if token.type == token_name and token.value in string:
            return True
    return False