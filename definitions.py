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