import ply.yacc as yacc
from lexer import tokens


def p_toml(p):
    "toml : top_level tables"

    #add to dict
    p[1].update(p[2])

    p[0] = p[1]
    #print("## toml\n" ,p[0], "\n")

def p_top_level(p):
    "top_level : properties"
    p[0] = p[1]
    #print("## top level\n", p[0], "\n")

def p_top_level_empty(p):
    "top_level : "
    p[0] = {}
    #print("## top level empty\n")

def p_tables(p):
    "tables : tables table"

    #add to tables
    p[1].update(p[2])

    p[0] = p[1]
    #print("## tables\n",p[0], "\n")

def p_tables_empty(p):
    "tables : "
    p[0] = {}
    #print("## tables empty\n", p[0], "\n")

def p_table(p):
    "table : LSQBRACKET key RSQBRACKET properties"
    p[0] = {p[2]:p[4]}
    #print("## table\n", p[0], "\n")
    
def p_table_no_properties(p):
    "table : LSQBRACKET key RSQBRACKET"
    p[0] = {p[2]:{}}
    #print("## table\n", p[0], "\n")

def p_table_array(p):
    "table : LSQBRACKET LSQBRACKET key RSQBRACKET RSQBRACKET properties"
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + "\n" + p[6]
    #print("## table array\n", p[0], "\n")

def p_table_array_no_properties(p):
    "table : LSQBRACKET LSQBRACKET key RSQBRACKET RSQBRACKET"
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
    print("## table array\n", p[0], "\n")

def p_properties(p):
    "properties : properties property"

    key = p[2][0]
    value = p[2][1]

    #add to properties
    p[1][key] = value

    p[0] = p[1]
    #print("## properties\n", p[0], "\n")

def p_properties_one(p):
    "properties : property"
    key = p[1][0]
    value = p[1][1]
    p[0] = {key: value}
    #print("## properties one\n", p[0], "\n")

def p_property(p):
    "property : key EQUALS value"
    p[0] = (p[1],p[3])
    #print("## property\n", p[0], "\n")

def p_key(p):
    "key : key DOT key_term"
    p[0] = p[1] + p[2] + p[3]
    #print(p[0], " - key dotted")

def p_key_one(p):
    "key : key_term"
    p[0] = p[1]
    #print(p[0], " - key one")

def p_key_term_bare(p):
    "key_term : BARE_KEY"
    p[0] = p[1]
    #print(p[0], " - bare key")

def p_key_term_string(p):
    "key_term : STRING_KEY"
    p[0] = p[1]
    #print(p[0], " - string key")

def p_key_term_string_literal(p):
    "key_term : STRING_LITERAL_KEY"
    p[0] = p[1]
    #print(p[0], " - string literal key")

def p_value_string(p):
    "value : STRING"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_string_literal(p):
    "value : STRING_LITERAL"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_multiline_string(p):
    "value : MULTILINE_STRING"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_multiline_string_literal(p):
    "value : MULTILINE_STRING_LITERAL"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_OCTAL(p):
    "value : OCTAL"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_FLOAT(p):
    "value : FLOAT"
    p[0] = str(p[1])
    #print(p[0], " - value")

def p_value_BOOL(p):
    "value : BOOL"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_HEXADECIMAL(p):
    "value : HEXADECIMAL"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_INTEGER(p):
    "value : INTEGER"
    p[0] = str(p[1])
    #print(p[0], " - value")

def p_value_BINARY(p):
    "value : BINARY"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_OFFSET_DATETIME(p):
    "value : OFFSET_DATETIME"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_LOCAL_DATETIME(p):
    "value : LOCAL_DATETIME"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_LOCAL_DATE(p):
    "value : LOCAL_DATE"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_LOCAL_TIME(p):
    "value : LOCAL_TIME"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_list(p):
    "value : list"
    p[0] = p[1]
    #print(p[0], " - value")

def p_value_inline_table(p):
    "value : inline_table"
    p[0] = p[1]
    #print(p[0], " - value")

def p_list(p):
    "list : LSQBRACKET list_values RSQBRACKET"
    p[0] = p[2]
    #print(p[0], " - list")

def p_list_values(p):
    "list_values : list_values COMMA value"
    p[0] = [p[1],p[3]]
    #print(p[0], " - list_values")

def p_list_values_one(p): 
    "list_values : value"
    p[0] = p[1]
    #print(p[0], " - list_values one")

def p_inline_table(p):
    "inline_table : LBRACKET properties RBRACKET"
    p[0] = p[2]
    #print(p[0], " - inline table")

def p_error(p):
    #print(f"Syntax error in input! - {p}")
    parser.success=False
    

parser = yacc.yacc()
parser.success = True

source2 = """

# This is a TOML document

title = "TOML Example"

[owner]
"name" = "Tom Preston-Werner"

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], "asd" ]
temp_targets = [ { yo = 2 }, "79.5", 72.0 ]

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"

[servers.beta.yep]

[[asd]]
bsd = "csd"

[[asd]]

"""

source = """

# This is a TOML document

title = "TOML Example"

[owner]
"name" = "Tom Preston-Werner"

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], "asd" ]
temp_targets = [ { yo = 2 }, "79.5", 72.0 ]

"""

result = parser.parse(source)

if parser.success:
    print("very cool")
else:
    print("no")

print(result)
