# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import MyLexer

def p_expression_plus(p):
    '''expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression '''
    p[0] = p[1] + p[3]

def p_expression_num(p):
    'expression : NUMBER'
    p[0] =  p[1]
def p_expression_lfparenthesis(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('group-expression',p[2])

def p_expression_head(p):
    'header : HEADER LBRACE list_expression RBRACE'
    p[0] = p[3]
def p_list_expression(p):
    """
    list_expression : list_expression NAME
                    | NAME
    """
    p[0] = p[1]
    if len(p) == 3:
        p[0] += p[2]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input! %s" % p.type

# Build the parser
tokens = MyLexer.tokens
parser = yacc.yacc(start="expression")

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: 
       continue
   result = parser.parse(s,lexer=MyLexer().lexer)
   print result