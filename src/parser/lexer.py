from enum import Enum

import ply.lex as lex
import re

from ply.lex import LexToken

from src.parser.exceptions import InvalidDatetimeFormat, UnexcapedBackslashException, IllegalCharacterException
from src.parser.utils import DateValidator, DateType


def validate_date_format(token: LexToken, fmt: DateType):

    valid, fmt = DateValidator(token.value, fmt).validate()

    if not valid:
        raise InvalidDatetimeFormat(token)

    return fmt


class GroupType(Enum):
    ARRAY = 0
    INLINE_TABLE = 1

class GroupStack:
    gt_stack: list

    def __init__(self):
        self.gt_stack = []

    def push(self, gt:GroupType):
        self.gt_stack.append(gt)

    def pop(self) -> GroupType|None:
        return self.gt_stack.pop() if len(self.gt_stack) > 0 else None

    def is_top_array(self) -> bool:
        return len(self.gt_stack)>0 and self.gt_stack[-1]==GroupType.ARRAY

    def is_top_inline_table(self) -> bool:
        return len(self.gt_stack)>0 and self.gt_stack[-1]==GroupType.INLINE_TABLE

    def is_empty(self):
        return len(self.gt_stack)==0

    def has_inline_table(self):
        for g in self.gt_stack:
            if g == GroupType.INLINE_TABLE:
                return True

        return False


class TomlLexer:

    # Building the lexer.
    def build(self, **kwargs):

        self.lexer = lex.lex(module=self, **kwargs, reflags=re.UNICODE | re.VERBOSE)
        self.lexer.group_stack = GroupStack()
        self.lexer.end = False
        self.lexer.is_end_of_statement = False
        self.lexer.capture_newlines = False

    def print_toks(self, data):

        self.lexer.input(data)

        for tok in self.lexer:
            print(tok)

    states = (
        ('VALUE', 'exclusive'),
    )

    tokens: tuple[str, ...] = (

        'RSQBRACKET', 'LSQBRACKET', 'DOUBLE_RSQBRACKET', 'DOUBLE_LSQBRACKET', 'RBRACKET', 'LBRACKET', 'STRING_LITERAL', 'HEXADECIMAL',
        'OFFSET_DATETIME', 'LOCAL_DATETIME', 'LOCAL_DATE', 'LOCAL_TIME', 'END_OF_LINE', 'END_OF_FILE','INTEGER',
        'BINARY', 'EQUALS', 'STRING', 'OCTAL', 'COMMA', 'FLOAT', 'BOOL', 'DOT', 'BARE_KEY',
        'STRING_KEY', 'STRING_LITERAL_KEY', 'MULTILINE_STRING', 'MULTILINE_STRING_LITERAL',

    )

    ########################################
    # Error and ignored token definitions. #
    ########################################

    t_ANY_ignore_COMMENT = r'\#.*'

    t_INITIAL_VALUE_ignore = ' \t\r\f\v'

    def t_ANY_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        raise IllegalCharacterException(t.value[0])
        #t.lexer.skip(1)

    #############################
    # End of line/file definitions.#
    #############################

    def t_ignore_INITIAL_LAST_WHITESPACE(self, t):
        r'\n+\Z'

    def t_ANY_END_OF_LINE(self, t):
        r'\n'
        if t.lexer.capture_newlines:
            if t.lexer.is_end_of_statement:
                t.lexer.is_end_of_statement = False
                t.lexer.capture_newlines = False
            return t
        else:
            return None

    def t_ANY_eof(self, t):
        if t.lexer.end:
            t.lexer.end = False
            t.lexer.is_end_of_statement = False
            t.lexer.capture_newlines = False
            return None
        t.lexer.end = True
        t.type = "END_OF_FILE"
        return t

    #############################
    # Syntax token definitions. #
    #############################

    t_ANY_COMMA = r'\,'
    t_ANY_DOT = r'\.'

    def t_ANY_LBRACKET(self, t):
        r'\{'
        t.lexer.begin('INITIAL')
        t.lexer.group_stack.push(GroupType.INLINE_TABLE)
        return t

    def t_INITIAL_RBRACKET(self, t):
        r'\}'
        t.lexer.group_stack.pop()
        if t.lexer.group_stack.is_top_array():
            t.lexer.begin('VALUE')
        elif t.lexer.group_stack.is_empty():
            t.lexer.is_end_of_statement = True
        return t

    def t_EQUALS(self, t):
        r'\='
        t.lexer.begin('VALUE')
        return t

    def t_INITIAL_DOUBLE_RSQBRACKET(self, t):
        r'\]\]'
        t.lexer.is_end_of_statement = True
        return t

    def t_INITIAL_DOUBLE_LSQBRACKET(self, t):
        r'\[\['
        t.lexer.capture_newlines = True
        return t

    def t_INITIAL_RSQBRACKET(self, t):
        r'\]'
        t.lexer.is_end_of_statement = True
        return t

    def t_INITIAL_LSQBRACKET(self, t):
        r'\['
        t.lexer.capture_newlines = True
        return t

    def t_VALUE_LSQBRACKET(self, t):
        r'\['
        if not t.lexer.group_stack.has_inline_table():
            t.lexer.capture_newlines = False
        t.lexer.group_stack.push(GroupType.ARRAY)
        return t

    def t_VALUE_RSQBRACKET(self, t):
        r'\]'
        t.lexer.group_stack.pop()
        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True
            t.lexer.capture_newlines = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.capture_newlines = True
            t.lexer.begin('INITIAL')

        return t

    ###########################
    # Keys token definitions. #
    ###########################

    def t_BARE_KEY(self, t):
        r'([a-zA-Z0-9_-]|[^\u0000-\u007F])+'
        t.lexer.capture_newlines = True
        return t

    def t_STRING_KEY(self, t):
        r'"([^\\\n]|\\.)*?"'
        t.value = t.value.removeprefix('"').removesuffix('"')
        t.lexer.capture_newlines = True
        return t

    def t_STRING_LITERAL_KEY(self, t):
        r"'.*?'"
        t.value = t.value.removeprefix("'").removesuffix("'")
        t.lexer.capture_newlines = True
        return t

    #############################
    # String token definitions. #
    #############################

    def t_VALUE_MULTILINE_STRING(self, t):
        r'"""([^\\]|(\\(.|\n))|\n)*?"{3,5}'

        t.value = t.value.removeprefix('"""').removesuffix('"""').removeprefix('\n')
        t.value = convert_escape_chars(t.value)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_MULTILINE_STRING_LITERAL(self, t):
        r"'''(.|\n)*?'{3,5}"

        t.value = t.value.removeprefix("'''").removesuffix("'''").removeprefix('\n')

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_STRING(self, t):
        r'"([^\\\n]|\\.)*?"'

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        t.value = t.value.removeprefix('"').removesuffix('"')

        t.value = convert_escape_chars(t.value)

        return t

    def t_VALUE_STRING_LITERAL(self, t):
        r"'.*?'"

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        t.value = t.value.removeprefix("'").removesuffix("'")

        return t


    ##############################################
    # Date, Time and Datetime token definitions. #
    ##############################################

    def t_VALUE_OFFSET_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}(:\d{2}(\.\d+)?)?([Zz]|([-+]\d{2}:\d{2})))'

        t.value = t.value.upper()

        formatted_as: str = validate_date_format(t, DateType.OFFSET_DATETIME)
        t.value = DateValidator.normalize(t.value, formatted_as, DateType.OFFSET_DATETIME)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_LOCAL_DATETIME(self, t):
        r'\d{4}-\d{2}-\d{2}[Tt ](\d{2}:\d{2}(:\d{2}(\.\d+)?)?)'

        t.value = t.value.upper()

        formatted_as: str = validate_date_format(t, DateType.LOCAL_DATETIME)
        t.value = DateValidator.normalize(t.value, formatted_as, DateType.LOCAL_DATETIME)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_LOCAL_DATE(self, t):
        r'\d{4}-\d{2}-\d{2}'

        formatted_as: str = validate_date_format(t, DateType.LOCAL_DATE)
        t.value = DateValidator.normalize(t.value, formatted_as, DateType.LOCAL_DATE)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_LOCAL_TIME(self, t):
        r'(\d{2}:\d{2}(:\d{2}(\.\d+)?)?)'

        formatted_as: str = validate_date_format(t, DateType.LOCAL_TIME)
        t.value = DateValidator.normalize(t.value, formatted_as, DateType.LOCAL_TIME)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    #############################
    # Number token definitions. #
    #############################

    def t_VALUE_HEXADECIMAL(self, t):
        r'0x[0-9A-Fa-f]([0-9A-Fa-f]|_[0-9A-Fa-f])*'

        t.value = int(t.value, 16)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_BINARY(self, t):
        r'0b[01]([01]|_[01])*'

        t.value = int(t.value, 2)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_OCTAL(self, t):
        r'0o[0-7]([0-7]|_[0-7])*'

        t.value = int(t.value, 8)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_FLOAT(self, t):
        r'((?=.*[eE\.])([-+]?(?:\d+(?:_\d+)*(?:\.\d*(?:_\d+)*)?|\.\d+(?:_\d+)*)(?:[eE][-+]?\d+(?:_\d+)*)?)((?:[eE\.][\d_+-]*))|((\+|\-)?nan)|((\+|\-)?inf))'

        t.value = float(t.value)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_INTEGER(self, t):
        r'(\+|-)?\d(\d|_\d)*'

        t.value = int(t.value)

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t

    def t_VALUE_BOOL(self, t):
        r'true|false'

        if t.lexer.group_stack.is_empty():
            t.lexer.begin('INITIAL')
            t.lexer.is_end_of_statement = True

        if t.lexer.group_stack.is_top_inline_table():
            t.lexer.begin('INITIAL')

        return t


def convert_escape_chars(s: str) -> str:
    esc = {
        r'b': '\b',
        r't': '\t',
        r'n': '\n',
        r'f': '\f',
        r'r': '\r',
        r'"': '\"',
        '\\': '\\'
    }
    multiline_bs_er = re.compile(r"\\\s*(\n|\r\n)\s*")
    i = 0
    while i < len(s) - 1:
        if s[i] == '\\':
            if s[i + 1] in esc:
                s = s[:i] + esc[s[i + 1]] + s[i + 2:]

            elif s[i + 1] == 'u':
                code = chr(int(s[i + 2:i + 6], 16))
                s = s[:i] + code + s[i + 6:]

            elif s[i + 1] == 'U':
                code = chr(int(s[i + 2:i + 10], 16))
                s = s[:i] + code + s[i + 10:]

            elif multiline_bs_er.match(s[i:]):
                s = multiline_bs_er.sub("", s, 1)
                continue

            else:
                raise UnexcapedBackslashException('In string: ' + s)
        i += 1

    return s


tLex = TomlLexer()
tLex.build()

tokens = tLex.tokens
lexer = tLex.lexer
