OPERATIONS = {
    '&': 'and',
    '*': 'call Math.multiply 2',
    '+': 'add',
    '-': 'sub',
    '/': 'call Math.divide 2',
    '|': 'or',
    '&lt;': 'lt',
    '=': 'eq',
    '&gt;': 'gt',
}

TYPES = [
    'boolean',
    'char',
    'int',
    'void',
]

SYMBOLS = "{}()[].,;+-*/&|<>=~"

KEYWORDS = TYPES + [
    'class',
    'constructor',
    'do',
    'else',
    'false',
    'field',
    'function',
    'if',
    'let',
    'method',
    'null',
    'return',
    'static',
    'this',
    'true',
    'var',
    'while',
]

NUMTABS = {
    "classVarDec": 1,
    "subroutineDec": 1,
    "parameterList": 2,
    "subroutineBody": 2,
    "statements": 3,
    "letStatement": 4,
    "ifStatement": 4,
    "whileStatement": 4,
    "doStatement": 4,
    "returnStatement": 4
}
