from datetime import datetime, date

import ply.lex as lex
from ply.lex import LexToken
from exceptions import InvalidDatetimeFormat


def validate_date_format(token: LexToken): 

    if datetime.strptime(token.value, '%Y-%m-%dT%H:%M:%S%z').tzinfo is not None:
        raise InvalidDatetimeFormat(token)
        
    # try:
    #     date.fromisoformat(token.value)
            
    # except ValueError:
    #     raise InvalidDatetimeFormat(token)

class TomlLexer:

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.array_num = 0

    def print_toks(self, data):
        self.lexer.input(data)
        for tok in self.lexer:
            print(tok)

    states = (
        ('VALUE', 'exclusive'),
    )

    tokens: tuple[str, ...] = (
        
        'RSQBRACKET', 'LSQBRACKET', 
        'RBRACKET', 'LBRACKET', 
        'STRING_LITERAL', # 
        'HEXADECIMAL',
        'OFFSET_DATETIME', 
        'LOCAL_DATETIME', 
        'LOCAL_DATE',
        'LOCAL_TIME',
        'COMMENT', 
        'INTEGER', 
        'BINARY',
        'EQUALS', 
        'STRING', #
        'OCTAL',
        'COMMA',
        'FLOAT', 
        'BOOL', 
        'DOT',
        'BARE_KEY',
        'STRING_KEY',
        'STRING_LITERAL_KEY',
        'MULTILINE_STRING',
        'MULTILINE_STRING_LITERAL',
        
    )
    
    # Literal token definiton.
    t_ANY_RBRACKET   = r'\}'
    t_ANY_COMMA      = r'\,'
    t_ANY_DOT        = r'\.'
    def t_ANY_LBRACKET(self, t): 
        r'\{'
        t.lexer.begin('INITIAL')
        return t

    def t_EQUALS(self, t):
        r'\='
        t.lexer.begin('VALUE')
        return t


    def t_RSQBRACKET(self, t):
        r'\]'
        return t

    def t_LSQBRACKET(self, t):
        r'\['
        return t


    def t_VALUE_LSQBRACKET(self, t):
        r'\['
        t.lexer.array_num += 1
        return t

    def t_VALUE_RSQBRACKET(self, t):
        r'\]'
        t.lexer.array_num -= 1
        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')
        return t

    # Misc

    t_ignore_COMMENT = r'\#.*'
    
    t_ANY_ignore = ' \t\n'

    def t_ANY_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    # Keys
        
    t_BARE_KEY = r'\w+'

    t_STRING_KEY = r'"([^\\]|\\.)*?"'

    t_STRING_LITERAL_KEY = r"'.*?'"


    # Values

    # Strings

    def t_VALUE_BOOL(self, t):
        r'true|false'
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t

    def t_VALUE_STRING(self, t):
        r'"([^\\]|\\.)*?"'
        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')
        return t

    def t_VALUE_STRING_LITERAL(self, t):
        r"'.*?'"
        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')
        return t

    def t_VALUE_MULTILINE_STRING(self, t):
        r'"""([^\\]|\\.|\n)*?"{3,5}'
        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')
        return t

    def t_VALUE_MULTILINE_STRING_LITERAL(self, t):
        r"'''(.|\n)*?'{3,5}"
        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')
        return t


    # Date token definiton.

    def t_VALUE_OFFSET_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|([-+]\d{2}:\d{2})))'
        validate_date_format(t)
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')

        return t
    
    
    def t_VALUE_LOCAL_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}:\d{2}(\.\d+)?)'
        validate_date_format(t)
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t
      
          
    def t_VALUE_LOCAL_DATE(self, t):
        r'\d{4}-\d{2}-\d{2}'
        validate_date_format(t)
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t
              
              
    def t_VALUE_LOCAL_TIME(self, t):
        r'(\d{2}:\d{2}:\d{2}(\.\d+)?)'
        validate_date_format(t)
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t
   

    # Number token definitions.
    def t_VALUE_FLOAT(self, t):
        r'(\+|-)?(\d(\d|_\d)*\.\d(\d|_\d)*([eE](\+|-)?\d(\d|_\d)*)?|nan|inf)'
        t.value = float(t.value)
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t

    def t_VALUE_INTEGER(self, t):
        r'(\+|-)?\d(\d|_\d)*'
        t.value = int(t.value)
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t
    
    
    def t_VALUE_HEXADECIMAL(self, t):
        r'0x[0-9A-Fa-f]([0-9A-Fa-f]|_[0-9A-Fa-f])*' 
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t
    
    
    def t_VALUE_BINARY(self, t):
        r'0b[01]([01]|_[01])*'
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t
        
    
    def t_VALUE_OCTAL(self, t):
        r'0o[0-7]([0-7]|_[0-9])*'
        if t.lexer.array_num==0:
            t.lexer.begin('INITIAL')
        return t

    
        
data = """

# This is a TOML document

title = "TOML Example"

[owner]
"name" = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], "asd" ]
temp_targets = { cpu = 79.5, case = 72.0 }

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"

"""
    
tLex = TomlLexer()

tLex.build()

tLex.print_toks(data)

    
    
