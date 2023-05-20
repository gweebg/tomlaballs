import ply.yacc as yacc

import json

from src.parser.lexer import tokens
from src.parser.utils import to_bool, TableArray, InlineTable


def insert_dotted_key_value_on_table(key, value, table):

    i: int = 0
    d = table

    while i < len(key):

        if isinstance(d, TableArray):
            d = d.get_last()

        elif isinstance(d, InlineTable) and d.is_locked:
            print("-- Error: cannot alter contents of inline table. key: ", key)
            parser.success = False
            return

        elif not isinstance(d, dict):
            print("-- Error: expected table to insert value of key: ", key)
            parser.success = False
            return

        if key[i] not in d:
            break

        d = d[key[i]]
        i += 1

    if i == len(key):
        print("-- Error: duplicate key found: ", key)
        parser.success = False
        return

    while i < len(key) - 1:
        d[key[i]] = {}
        d = d[key[i]]
        i += 1

    d[key[i]] = value


def insert_table_on_table_array(key, value, table):

    i = 0
    d = table

    while i < len(key):
        if isinstance(d, TableArray):
            d = d.get_last()

        elif isinstance(d, InlineTable) and d.is_locked:
            print("-- Error: cannot alter contents of inline table. key: ", key)
            parser.success = False
            return

        elif not isinstance(d, dict):
            print("-- Error: expected table to insert value of key: ", key)
            parser.success = False
            return

        if key[i] not in d:
            break

        d = d[key[i]]
        i += 1

    if i == len(key):
        if not isinstance(d, TableArray):
            print("-- Error: expected table array to insert value of key :", key)
            parser.success = False
            return
        d.append(value)

    else:
        while i < len(key) - 1:
            d[key[i]] = {}
            d = d[key[i]]
            i += 1
        
        ta = TableArray()
        ta.append(value)
        d[key[i]] = ta


def p_toml(p):
    "toml : top_level tables"

    # add to dict
    for key, value in p[1].items():
        insert_dotted_key_value_on_table(key, value, p[2])

    p[0] = p[2]
    print(p[0], " - toml")


def p_top_level(p):
    "top_level : properties"
    p[0] = p[1]
    print(p[0], " - top level")


def p_top_level_empty(p):
    "top_level : "
    p[0] = {}
    print(" - top level empty")


def p_tables(p):
    "tables : tables table"

    table_key = p[2][0]
    table_properties = p[2][1]

    insert_dotted_key_value_on_table(table_key, table_properties, p[1])

    p[0] = p[1]
    print(p[0], " - tables")

def p_tables_array_tables(p):
    "tables : tables table_array"

    array_key = p[2][0]
    array_table = p[2][1]

    insert_table_on_table_array(array_key, array_table, p[1])

    p[0] = p[1]
    print(p[0], " - tables")


def p_tables_empty(p):
    "tables : "
    p[0] = {}
    print(p[0], " - tables empty")


def p_table(p):
    "table : LSQBRACKET key RSQBRACKET line_terminator properties"
    p[0] = (p[2], p[5])
    print(p[0], " - table")


def p_table_no_properties(p):
    "table : LSQBRACKET key RSQBRACKET line_terminator"
    p[0] = (p[2], {})
    print(p[0], " - table")


def p_table_array(p):
    "table_array : LSQBRACKET LSQBRACKET key RSQBRACKET RSQBRACKET line_terminator properties"
    p[0] = (p[3], p[7])
    print(p[0], " - table array")


def p_table_array_no_properties(p):
    "table_array : LSQBRACKET LSQBRACKET key RSQBRACKET RSQBRACKET line_terminator"
    p[0] = (p[3], {})
    print(p[0], " - table array")


def p_properties(p):
    "properties : properties property line_terminator"

    key = p[2][0]
    value = p[2][1]

    insert_dotted_key_value_on_table(key, value, p[1])

    p[0] = p[1]
    print(p[0], " - properties")


def p_properties_one(p):
    "properties : property line_terminator"
    key = p[1][0]
    value = p[1][1]

    key.reverse()

    d = {key[0]: value}
    for i in range(1, len(key)):
        d = {key[i]: d}

    p[0] = d
    print(p[0], " - properties")


def p_property(p):
    "property : key EQUALS value"
    p[0] = (p[1], p[3])
    print(p[0], " - property")


def p_key(p):
    "key : key DOT key_term"
    p[1].append(p[3])
    p[0] = p[1]
    print(p[0], " - key dotted")


def p_key_one(p):
    "key : key_term"
    p[0] = [p[1]]
    print(p[0], " - key one")


def p_key_term_bare(p):
    "key_term : BARE_KEY"
    p[0] = p[1]
    print(p[0], " - bare key")


def p_key_term_string(p):
    "key_term : STRING_KEY"
    p[0] = p[1]
    print(p[0], " - string key")


def p_key_term_string_literal(p):
    "key_term : STRING_LITERAL_KEY"
    p[0] = p[1]
    print(p[0], " - string literal key")


def p_value_string(p):
    "value : STRING"
    p[0] = p[1]
    print(p[0], " - value string")


def p_value_string_literal(p):
    "value : STRING_LITERAL"
    p[0] = p[1]
    print(p[0], " - value string literal")


def p_value_multiline_string(p):
    "value : MULTILINE_STRING"
    p[0] = p[1]
    print(p[0], " - value multiline string")


def p_value_multiline_string_literal(p):
    "value : MULTILINE_STRING_LITERAL"
    p[0] = p[1]
    print(p[0], " - value multiline str literal")


def p_value_OCTAL(p):
    "value : OCTAL"
    p[0] = p[1]
    print(p[0], " - value octal")


def p_value_FLOAT(p):
    "value : FLOAT"
    p[0] = p[1]
    print(p[0], " - value float")


def p_value_BOOL(p):
    "value : BOOL"
    p[0] = to_bool(p[1])
    print(p[0], " - value bool")


def p_value_HEXADECIMAL(p):
    "value : HEXADECIMAL"
    p[0] = p[1]
    print(p[0], " - value hex")


def p_value_INTEGER(p):
    "value : INTEGER"
    p[0] = p[1]
    print(p[0], " - value integer")


def p_value_BINARY(p):
    "value : BINARY"
    p[0] = p[1]
    print(p[0], " - value binary")


def p_value_OFFSET_DATETIME(p):
    "value : OFFSET_DATETIME"
    p[0] = p[1]
    print(p[0], " - value offset datetime")


def p_value_LOCAL_DATETIME(p):
    "value : LOCAL_DATETIME"
    p[0] = p[1]
    print(p[0], " - value local datetime")


def p_value_LOCAL_DATE(p):
    "value : LOCAL_DATE"
    p[0] = p[1]
    print(p[0], " - value local date")


def p_value_LOCAL_TIME(p):
    "value : LOCAL_TIME"
    p[0] = p[1]
    print(p[0], " - value local time")


def p_value_list(p):
    "value : list"
    p[0] = p[1]
    print(p[0], " - value list")


def p_value_inline_table(p):
    "value : inline_table"
    p[0] = p[1]
    print(p[0], " - value it")


def p_list(p):
    "list : LSQBRACKET list_values RSQBRACKET"
    p[0] = p[2]
    print(p[0], " - list")


def p_list_comma(p):
    "list : LSQBRACKET list_values COMMA RSQBRACKET"
    p[0] = p[2]
    print(p[0], " - list")


def p_list_empty(p):
    "list : LSQBRACKET RSQBRACKET"
    p[0] = []
    print(p[0], " - list")


def p_list_values(p):
    "list_values : list_values COMMA value"
    p[1].append(p[3])
    p[0] = p[1]
    print(p[0], " - list_values")


def p_list_values_one(p):
    "list_values : value"
    p[0] = [p[1]]
    print(p[0], " - list_values one")


def p_inline_table(p):
    "inline_table : LBRACKET it_properties RBRACKET"
    p[2].is_locked = True
    p[0] = p[2]
    print(p[0], " - inline table")

def p_inline_table_empty(p):
    "inline_table : LBRACKET RBRACKET"
    p[0] = InlineTable()
    print(p[0], " - inline table")

def p_it_properties(p):
    "it_properties : it_properties COMMA property"

    key = p[3][0]
    value = p[3][1]

    insert_dotted_key_value_on_table(key, value, p[1])

    p[0] = p[1]
    print(p[0], " - it_properties")

def p_it_properties_one(p):
    "it_properties : property"

    key = p[1][0]
    value = p[1][1]

    key.reverse()

    d = InlineTable()
    d[key[0]] = value

    for i in range(1, len(key)):
        td = InlineTable()
        td[key[i]] = d
        d = td

    p[0] = d
    print(p[0], " - it_properties")

def p_line_terminator(p):
    """line_terminator : END_OF_LINE
                        | END_OF_FILE"""
    print("end of line")

def p_error(p):
    print(f"Syntax error in input! - {p}")
    parser.success = False


parser = yacc.yacc()
parser.success = True

source = """
# This is a TOML document

title = "TOML Example"
list = [ " \\", ",]
table = {value1 = 1, value2 = 2, value3 = "asd"}
void = [[[[[]]]]] 
ints = [
    1,
    2, #this is ok
]

[owner]
name = "Tom Preston-Werner"

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], [3.14] ]
temp_targets = { cpu = 79.5 }

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"

[[arr]]
bsd = "csd"
e = 3

[arr.adhfs]
s = 2
t = 4

[[arr.yep]]
dsa = 2
g = 2

"""

source2 = '''
a = {aa = "asd"}
a.bb = 2
'''

#import sys
#
#for line in sys.stdin:
#    source2 += line
#    print("line: ", line)

#result = parser.parse(source2)
#
#if parser.success:
#    print(json.dumps(result, indent=2))
#else:
#    print("Parsing unsuccessful")

#import tomllib
#
#print("toml lib:\n", json.dumps(tomllib.loads(source2)))
