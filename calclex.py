import ply.lex as lex
class MyLexer:

    reserved = ['HEADER']
    tokens = [
        "NUMBER",
        "PLUS",
        "MINUS",
        "DIVIDE",
        "TIMES",
        "LPAREN",
        "RPAREN",
        "NAME",
        "LBRACE",
        "RBRACE",
        "SPECIFIC",
    ]
    tokens = tokens + reserved

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_DIVIDE = r'\/'
    t_TIMES = r'\*'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = ' \t'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'

    def __init__(self):
        self.lexer = lex.lex(module=self)
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        t.type = "SPECIFIC"
        return t

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value.upper() in self.reserved:
            t.type = t.value.upper() 
        return t

    def t_error(self, t):
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

data = '''
    3+4*10+  (3+4)
'''


lexer = lex.lex(object = MyLexer())
lexer.input(data)
while True:
    tok = lexer.token()
    if tok:
        print tok
    else:
        break