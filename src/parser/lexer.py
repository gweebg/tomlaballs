import ply.lex as lex
import re

from ply.lex import LexToken

from exceptions import InvalidDatetimeFormat
from utils import DateValidator, DateType


def validate_date_format(token: LexToken, fmt: DateType):

    valid, fmt = DateValidator(token.value, fmt).validate()

    if not valid:
        raise InvalidDatetimeFormat(token)

    return fmt


class TomlLexer:

    # Building the lexer.
    def build(self, **kwargs):

        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.array_num = 0
        self.lexer.inline_table_num = 0

    def print_toks(self, data):

        self.lexer.input(data)

        for tok in self.lexer:
            print(tok)

    states = (
        ('VALUE', 'exclusive'),
    )

    tokens: tuple[str, ...] = (

        'RSQBRACKET', 'LSQBRACKET', 'RBRACKET', 'LBRACKET', 'STRING_LITERAL', 'HEXADECIMAL',
        'OFFSET_DATETIME', 'LOCAL_DATETIME', 'LOCAL_DATE', 'LOCAL_TIME', 'COMMENT', 'INTEGER',
        'BINARY', 'EQUALS', 'STRING', 'OCTAL', 'COMMA', 'FLOAT', 'BOOL', 'DOT', 'BARE_KEY',
        'STRING_KEY', 'STRING_LITERAL_KEY', 'MULTILINE_STRING', 'MULTILINE_STRING_LITERAL',

    )

    #############################
    # Syntax token definitions. #
    #############################

    t_ANY_COMMA = r'\,'
    t_ANY_DOT = r'\.'

    def t_ANY_LBRACKET(self, t):
        r'\{'
        t.lexer.begin('INITIAL')
        t.lexer.inline_table_num += 1
        return t

    def t_ANY_RBRACKET(self, t):
        r'\}'
        t.lexer.inline_table_num -= 1
        if t.lexer.inline_table_num == 0 and t.lexer.array_num > 0:
            t.lexer.begin('VALUE')
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

    ########################################
    # Error and ignored token definitions. #
    ########################################

    t_ANY_ignore_COMMENT = r'\#.*'

    t_ANY_ignore = ' \t\n'

    def t_ANY_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        # raise IllegalCharacterException(t.value[0])
        t.lexer.skip(1)

    ###########################
    # Keys token definitions. #
    ###########################

    t_BARE_KEY = r'[a-zA-Z0-9_-]+'

    def t_STRING_KEY(self, t):
        r'"([^\\]|\\.)*?"'
        t.value = t.value.rstrip('"').lstrip('"')
        return t

    def t_STRING_LITERAL_KEY(self, t):
        r"'.*?'"
        t.value = t.value.rstrip("'").lstrip("'")
        return t

    #############################
    # String token definitions. #
    #############################

    def t_VALUE_STRING(self, t):
        r'"([^\\]|\\.)*?"'

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        t.value = t.value.rstrip('"').lstrip('"')

        return t

    def t_VALUE_STRING_LITERAL(self, t):
        r"'.*?'"

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        t.value = str(t.value).replace("'", "")

        return t

    def t_VALUE_MULTILINE_STRING(self, t):
        r'"""([^\\]|\\(.|\n)|\n)*?"{3,5}"""([^\\]|\\(.|\n)|\n)*?"{3,5}'

        t.value = re.sub(r"\\(\n|\r\n)\s+", "", t.value)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_MULTILINE_STRING_LITERAL(self, t):
        r"'''(.|\n)*?'{3,5}"

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    ##############################################
    # Date, Time and Datetime token definitions. #
    ##############################################

    def t_VALUE_OFFSET_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}(:\d{2}(\.\d+)?)?([Zz]|([-+]\d{2}:\d{2})))'

        t.value = t.value.upper()

        print("OFFSET DATETIME")

        formatted_as: str = validate_date_format(t, DateType.OFFSET_DATETIME)
        t.value = DateValidator.normalize(t.value, formatted_as, DateType.OFFSET_DATETIME)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_LOCAL_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}(:\d{2}(\.\d+)?)?)'

        t.value = t.value.upper()

        formatted_as: str = validate_date_format(t, DateType.LOCAL_DATETIME)
        t.value = DateValidator.normalize(t.value, formatted_as, DateType.LOCAL_DATETIME)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_LOCAL_DATE(self, t):
        r'\d{4}-\d{2}-\d{2}'

        validate_date_format(t, DateType.LOCAL_DATE)
        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_LOCAL_TIME(self, t):
        r'(\d{2}:\d{2}(:\d{2}(\.\d+)?)?)'

        formatted_as: str = validate_date_format(t, DateType.LOCAL_TIME)
        t.value = DateValidator.normalize(t.value, formatted_as, DateType.LOCAL_TIME)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    #############################
    # Number token definitions. #
    #############################

    def t_VALUE_HEXADECIMAL(self, t):
        r'0x[0-9A-Fa-f]([0-9A-Fa-f]|_[0-9A-Fa-f])*'

        t.value = int(t.value, 16)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_BINARY(self, t):
        r'0b[01]([01]|_[01])*'

        t.value = int(t.value, 2)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_OCTAL(self, t):
        r'0o[0-7]([0-7]|_[0-9])*'

        t.value = int(t.value, 8)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_FLOAT(self, t):
        r'((?=.*[eE\.])([-+]?(?:\d+(?:_\d+)*(?:\.\d*(?:_\d+)*)?|\.\d+(?:_\d+)*)(?:[eE][-+]?\d+(?:_\d+)*)?)((?:[eE\.][\d_+-]*))|((\+|\-)?nan)|((\+|\-)?inf))'

        t.value = float(t.value)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_INTEGER(self, t):
        r'(\+|-)?\d(\d|_\d)*'

        t.value = int(t.value)

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_BOOL(self, t):
        r'true|false'

        if t.lexer.array_num == 0:
            t.lexer.begin('INITIAL')

        return t


tLex = TomlLexer()
tLex.build()

tokens = tLex.tokens
lexer = tLex.lexer
