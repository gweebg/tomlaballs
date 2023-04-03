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
    
    tokens: tuple[str] = (
        
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
        'OCTAL'
        'COMMA',
        'FLOAT', 
        'BOOL', 
        'DOT'
        
    )
    
    # Literal token definiton.
    t_RSQBRACKET = r'\]'
    t_LSQBRACKET = r'\['
    t_RBRACKET   = r'\}'
    t_LBRACKET   = r'\{'
    t_EQUALS     = r'\='
    t_COMMA      = r'\,'
    t_DOT        = r'\.'
    
    # Date token definiton.
    def t_OFFSET_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|([-+]\d{2}:\d{2})))'
        validate_date_format(t)
        return t
    
    
    def t_LOCAL_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}:\d{2}(\.\d+)?)'
        validate_date_format(t)
        return t
      
          
    def t_LOCAL_DATE(self, t):
        r'\d{4}-\d{2}-\d{2}'
        validate_date_format(t)
        return t
              
              
    def t_LOCAL_TIME(self, t):
        r'(\d{2}:\d{2}:\d{2}(\.\d+)?)'
        validate_date_format(t)
        return t
   

    # Number token definitions.
    def t_INTEGER(self, t):
        r'(\+|-)?\d(\d|_\d)*'
        t.value = int(t.value)
        return t
    
    
    def t_HEXADECIMAL(self, t):
        r'0x[0-9A-Fa-f]([0-9A-Fa-f]|_[0-9A-Fa-f])*' 
        return t
    
    
    def t_BINARY(self, t):
        r'0b[01]([01]|_[01])*'
        return t
        
    
    def t_OCTAL(self, t):
        r'0o[0-7]([0-7]|_[0-9])*'
        return t
    
    
    def t_FLOAT(self, t):
        r'(\+|-)?(\d(\d|_\d)*\.\d(\d|_\d)*([eE](\+|-)?\d(\d|_\d)*)?|nan|inf)'
        t.value = float(t.value)
        return t
    
    
    
        
    


    
    
