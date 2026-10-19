import pytest

from jerison_lang.scanner import Scanner, Token, TokenType

T = TokenType

def pytest_generate_tests(metafunc):
    if metafunc.cls is not None and hasattr(metafunc.cls, "cases"):
        metafunc.parametrize(
            ("source", "expected"),
            metafunc.cls.cases[metafunc.function.__name__],
        )


def check_tokens(source: str, expected: list[Token]):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    valid_line = True
    for token_one, token_two in zip(tokens, expected):
        print(f"{token_one} {token_one.line}// {token_two} {token_two.line}")
        if token_one.line != token_two.line:
            valid_line = False
    assert tokens == expected and valid_line


class BaseScannerTest:
    cases = {
        "test_single": [],
        "test_pairs": [],
        "test_sequences": [],
        "test_edge_cases": [],
    }

    def test_single(self, source: str, expected: list[Token]):
        check_tokens(source, expected)

    def test_pairs(self, source: str, expected: list[Token]):
        check_tokens(source, expected)

    def test_sequences(self, source: str, expected: list[Token]):
        check_tokens(source, expected)

    def test_edge_cases(self, source: str, expected: list[Token]):
        check_tokens(source, expected)


SINGLES = [
    ("(", [Token(T.LEFT_PAREN, "(", None, 1), Token(T.EOF, "", None, 1)]),
    (")", [Token(T.RIGHT_PAREN, ")", None, 1), Token(T.EOF, "", None, 1)]),
    ("{", [Token(T.LEFT_BRACE, "{", None, 1), Token(T.EOF, "", None, 1)]),
    ("}", [Token(T.RIGHT_BRACE, "}", None, 1), Token(T.EOF, "", None, 1)]),
]

PAIRS = [
    (
        "()",
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "{}",
        [
            Token(T.LEFT_BRACE, "{", None, 1),
            Token(T.RIGHT_BRACE, "}", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        ",.",
        [
            Token(T.COMMA, ",", None, 1),
            Token(T.DOT, ".", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "+-",
        [
            Token(T.PLUS, "+", None, 1),
            Token(T.MINUS, "-", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
]

SEQUENCES = [
    (
        "(){},.-+;*",
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.LEFT_BRACE, "{", None, 1),
            Token(T.RIGHT_BRACE, "}", None, 1),
            Token(T.COMMA, ",", None, 1),
            Token(T.DOT, ".", None, 1),
            Token(T.MINUS, "-", None, 1),
            Token(T.PLUS, "+", None, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.STAR, "*", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "*;+-.,}{)(",
        [
            Token(T.STAR, "*", None, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.PLUS, "+", None, 1),
            Token(T.MINUS, "-", None, 1),
            Token(T.DOT, ".", None, 1),
            Token(T.COMMA, ",", None, 1),
            Token(T.RIGHT_BRACE, "}", None, 1),
            Token(T.LEFT_BRACE, "{", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "{(;)}",
        [
            Token(T.LEFT_BRACE, "{", None, 1),
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.RIGHT_BRACE, "}", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "( + )\n{ * }",
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.PLUS, "+", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.LEFT_BRACE, "{", None, 2),
            Token(T.STAR, "*", None, 2),
            Token(T.RIGHT_BRACE, "}", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
]

EDGE_CASES = [
    ("", [Token(T.EOF, "", None, 1)]),
    (" \t\r\n", [Token(T.EOF, "", None, 2)]),
    (
        "---",
        [
            Token(T.MINUS, "-", None, 1),
            Token(T.MINUS, "-", None, 1),
            Token(T.MINUS, "-", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    ("*" * 1000, [Token(T.STAR, "*", None, 1)] * 1000 + [Token(T.EOF, "", None, 1)]),
]

class TestSingleCharacterTokens(BaseScannerTest):
    cases = {
        "test_single": SINGLES,
        "test_pairs": PAIRS,
        "test_sequences": SEQUENCES,
        "test_edge_cases": EDGE_CASES,
    }

OPERATOR_SINGLES = [
    ("!", [Token(T.BANG, "!", None, 1), Token(T.EOF, "", None, 1)]),
    ("=", [Token(T.EQUAL, "=", None, 1), Token(T.EOF, "", None, 1)]),
    ("<", [Token(T.LESS, "<", None, 1), Token(T.EOF, "", None, 1)]),
    (">", [Token(T.GREATER, ">", None, 1), Token(T.EOF, "", None, 1)]),
]

OPERATOR_PAIRS = [
    ("!=", [Token(T.BANG_EQUAL, "!=", None, 1), Token(T.EOF, "", None, 1)]),
    ("==", [Token(T.EQUAL_EQUAL, "==", None, 1), Token(T.EOF, "", None, 1)]),
    ("<=", [Token(T.LESS_EQUAL, "<=", None, 1), Token(T.EOF, "", None, 1)]),
    (">=", [Token(T.GREATER_EQUAL, ">=", None, 1), Token(T.EOF, "", None, 1)]),
]

OPERATOR_SEQUENCES = [
    (
        "!=<>=",
        [
            Token(T.BANG_EQUAL, "!=", None, 1),
            Token(T.LESS, "<", None, 1),
            Token(T.GREATER_EQUAL, ">=", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "==!=<=>=",
        [
            Token(T.EQUAL_EQUAL, "==", None, 1),
            Token(T.BANG_EQUAL, "!=", None, 1),
            Token(T.LESS_EQUAL, "<=", None, 1),
            Token(T.GREATER_EQUAL, ">=", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "! = < >",
        [
            Token(T.BANG, "!", None, 1),
            Token(T.EQUAL, "=", None, 1),
            Token(T.LESS, "<", None, 1),
            Token(T.GREATER, ">", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
]

OPERATOR_EDGE_CASES = [
    (
        "!==",
        [
            Token(T.BANG_EQUAL, "!=", None, 1),
            Token(T.EQUAL, "=", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "===",
        [
            Token(T.EQUAL_EQUAL, "==", None, 1),
            Token(T.EQUAL, "=", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "<<=",
        [
            Token(T.LESS, "<", None, 1),
            Token(T.LESS_EQUAL, "<=", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "!\n=",
        [
            Token(T.BANG, "!", None, 1),
            Token(T.EQUAL, "=", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
]

class TestOperatorCharacterTokens(BaseScannerTest):
    cases = {
        "test_single": OPERATOR_SINGLES,
        "test_pairs": OPERATOR_PAIRS,
        "test_sequences": OPERATOR_SEQUENCES,
        "test_edge_cases": OPERATOR_EDGE_CASES,
    }

COMMENT_WS_SINGLES = [
    ("/", [Token(T.SLASH, "/", None, 1), Token(T.EOF, "", None, 1)]),
    ("// comment", [Token(T.EOF, "", None, 1)]),
    (" ", [Token(T.EOF, "", None, 1)]),
    ("\t", [Token(T.EOF, "", None, 1)]),
    ("\r", [Token(T.EOF, "", None, 1)]),
    ("\n", [Token(T.EOF, "", None, 2)]),
]

COMMENT_WS_PAIRS = [
    ("//", [Token(T.EOF, "", None, 1)]),
    (
        "/ /",
        [
            Token(T.SLASH, "/", None, 1),
            Token(T.SLASH, "/", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (" \t", [Token(T.EOF, "", None, 1)]),
    ("\r\n", [Token(T.EOF, "", None, 2)]),
]

COMMENT_WS_SEQUENCES = [
    (
        "(/)",
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.SLASH, "/", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "<= / >=",
        [
            Token(T.LESS_EQUAL, "<=", None, 1),
            Token(T.SLASH, "/", None, 1),
            Token(T.GREATER_EQUAL, ">=", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "{\t*\r}",
        [
            Token(T.LEFT_BRACE, "{", None, 1),
            Token(T.STAR, "*", None, 1),
            Token(T.RIGHT_BRACE, "}", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "!= // not equal\n;",
        [
            Token(T.BANG_EQUAL, "!=", None, 1),
            Token(T.SEMICOLON, ";", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
    (
        "( // open\n)",
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
]

COMMENT_WS_EDGE_CASES = [
    ("( // no newline after", [Token(T.LEFT_PAREN, "(", None, 1), Token(T.EOF, "", None, 1)]),
    ("\n\n\n", [Token(T.EOF, "", None, 4)]),
    (
        "(\n\n)",
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 3),
            Token(T.EOF, "", None, 3),
        ],
    ),
    (
        "/(",
        [
            Token(T.SLASH, "/", None, 1),
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "/=",
        [
            Token(T.SLASH, "/", None, 1),
            Token(T.EQUAL, "=", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "// a // b\n;",
        [
            Token(T.SEMICOLON, ";", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
    (" \t\r\n \t", [Token(T.EOF, "", None, 2)]),
]

class TestCommentWSCharacterTokens(BaseScannerTest):
    cases = {
        "test_single": COMMENT_WS_SINGLES,
        "test_pairs": COMMENT_WS_PAIRS,
        "test_sequences": COMMENT_WS_SEQUENCES,
        "test_edge_cases": COMMENT_WS_EDGE_CASES,
    }

LITERAL_SINGLES = [
    ("0", [Token(T.NUMBER, "0", 0.0, 1), Token(T.EOF, "", None, 1)]),
    ("123", [Token(T.NUMBER, "123", 123.0, 1), Token(T.EOF, "", None, 1)]),
    ("4567", [Token(T.NUMBER, "4567", 4567.0, 1), Token(T.EOF, "", None, 1)]),
    ("123.456", [Token(T.NUMBER, "123.456", 123.456, 1), Token(T.EOF, "", None, 1)]),
    ("0.5", [Token(T.NUMBER, "0.5", 0.5, 1), Token(T.EOF, "", None, 1)]),
    ("3.14159", [Token(T.NUMBER, "3.14159", 3.14159, 1), Token(T.EOF, "", None, 1)]),
    ('"hello"', [Token(T.STRING, '"hello"', "hello", 1), Token(T.EOF, "", None, 1)]),
    ('"hello world"', [Token(T.STRING, '"hello world"', "hello world", 1), Token(T.EOF, "", None, 1)]),
    ('""', [Token(T.STRING, '""', "", 1), Token(T.EOF, "", None, 1)]),
    ('" "', [Token(T.STRING, '" "', " ", 1), Token(T.EOF, "", None, 1)]),
]

LITERAL_PAIRS = [
    (
        "1 2",
        [
            Token(T.NUMBER, "1", 1.0, 1),
            Token(T.NUMBER, "2", 2.0, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "-5",
        [
            Token(T.MINUS, "-", None, 1),
            Token(T.NUMBER, "5", 5.0, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        '"a""b"',
        [
            Token(T.STRING, '"a"', "a", 1),
            Token(T.STRING, '"b"', "b", 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        '"a" "b"',
        [
            Token(T.STRING, '"a"', "a", 1),
            Token(T.STRING, '"b"', "b", 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
]

LITERAL_SEQUENCES = [
    (
        "1+2.5",
        [
            Token(T.NUMBER, "1", 1.0, 1),
            Token(T.PLUS, "+", None, 1),
            Token(T.NUMBER, "2.5", 2.5, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "(3.5) >= 0",
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.NUMBER, "3.5", 3.5, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.GREATER_EQUAL, ">=", None, 1),
            Token(T.NUMBER, "0", 0.0, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "1\n2",
        [
            Token(T.NUMBER, "1", 1.0, 1),
            Token(T.NUMBER, "2", 2.0, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
    (
        '("hi")',
        [
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.STRING, '"hi"', "hi", 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        '"a" + "b";',
        [
            Token(T.STRING, '"a"', "a", 1),
            Token(T.PLUS, "+", None, 1),
            Token(T.STRING, '"b"', "b", 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        '"x" != 1',
        [
            Token(T.STRING, '"x"', "x", 1),
            Token(T.BANG_EQUAL, "!=", None, 1),
            Token(T.NUMBER, "1", 1.0, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
]

LITERAL_EDGE_CASES = [
    ("0.0", [Token(T.NUMBER, "0.0", 0.0, 1), Token(T.EOF, "", None, 1)]),
    ("999999", [Token(T.NUMBER, "999999", 999999.0, 1), Token(T.EOF, "", None, 1)]),
    (r'"\"', [Token(T.STRING, r'"\"', "\\", 1), Token(T.EOF, "", None, 1)]),
    (r'"a\nb"', [Token(T.STRING, r'"a\nb"', r"a\nb", 1), Token(T.EOF, "", None, 1)]),
    (r'"a\tb"', [Token(T.STRING, r'"a\tb"', r"a\tb", 1), Token(T.EOF, "", None, 1)]),
    ('"a\nb"', [Token(T.STRING, '"a\nb"', "a\nb", 2), Token(T.EOF, "", None, 2)]),
    ('"// not a comment"', [Token(T.STRING, '"// not a comment"', "// not a comment", 1), Token(T.EOF, "", None, 1)]),
    ('"123"', [Token(T.STRING, '"123"', "123", 1), Token(T.EOF, "", None, 1)]),
]

class TestLiteralTokens(BaseScannerTest):
    cases = {
        "test_single": LITERAL_SINGLES,
        "test_pairs": LITERAL_PAIRS,
        "test_sequences": LITERAL_SEQUENCES,
        "test_edge_cases": LITERAL_EDGE_CASES,
    }

KEYWORD_SINGLES = [
    ("and", [Token(T.AND, "and", None, 1), Token(T.EOF, "", None, 1)]),
    ("class", [Token(T.CLASS, "class", None, 1), Token(T.EOF, "", None, 1)]),
    ("else", [Token(T.ELSE, "else", None, 1), Token(T.EOF, "", None, 1)]),
    ("false", [Token(T.FALSE, "false", None, 1), Token(T.EOF, "", None, 1)]),
    ("for", [Token(T.FOR, "for", None, 1), Token(T.EOF, "", None, 1)]),
    ("fun", [Token(T.FUN, "fun", None, 1), Token(T.EOF, "", None, 1)]),
    ("if", [Token(T.IF, "if", None, 1), Token(T.EOF, "", None, 1)]),
    ("nil", [Token(T.NIL, "nil", None, 1), Token(T.EOF, "", None, 1)]),
    ("or", [Token(T.OR, "or", None, 1), Token(T.EOF, "", None, 1)]),
    ("print", [Token(T.PRINT, "print", None, 1), Token(T.EOF, "", None, 1)]),
    ("return", [Token(T.RETURN, "return", None, 1), Token(T.EOF, "", None, 1)]),
    ("super", [Token(T.SUPER, "super", None, 1), Token(T.EOF, "", None, 1)]),
    ("this", [Token(T.THIS, "this", None, 1), Token(T.EOF, "", None, 1)]),
    ("true", [Token(T.TRUE, "true", None, 1), Token(T.EOF, "", None, 1)]),
    ("var", [Token(T.VAR, "var", None, 1), Token(T.EOF, "", None, 1)]),
    ("while", [Token(T.WHILE, "while", None, 1), Token(T.EOF, "", None, 1)]),
]

KEYWORD_PAIRS = [
    (
        "true false",
        [
            Token(T.TRUE, "true", None, 1),
            Token(T.FALSE, "false", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "if else",
        [
            Token(T.IF, "if", None, 1),
            Token(T.ELSE, "else", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "and or",
        [
            Token(T.AND, "and", None, 1),
            Token(T.OR, "or", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "this\nsuper",
        [
            Token(T.THIS, "this", None, 1),
            Token(T.SUPER, "super", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
]

KEYWORD_SEQUENCES = [
    (
        "print nil;",
        [
            Token(T.PRINT, "print", None, 1),
            Token(T.NIL, "nil", None, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "while (true) return;",
        [
            Token(T.WHILE, "while", None, 1),
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.TRUE, "true", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.RETURN, "return", None, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "class fun var for",
        [
            Token(T.CLASS, "class", None, 1),
            Token(T.FUN, "fun", None, 1),
            Token(T.VAR, "var", None, 1),
            Token(T.FOR, "for", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
]

KEYWORD_EDGE_CASES = [
    ("orchid", [Token(T.IDENTIFIER, "orchid", None, 1), Token(T.EOF, "", None, 1)]),
    ("classy", [Token(T.IDENTIFIER, "classy", None, 1), Token(T.EOF, "", None, 1)]),
    ("nil_", [Token(T.IDENTIFIER, "nil_", None, 1), Token(T.EOF, "", None, 1)]),
    ("for1", [Token(T.IDENTIFIER, "for1", None, 1), Token(T.EOF, "", None, 1)]),
    ("And", [Token(T.IDENTIFIER, "And", None, 1), Token(T.EOF, "", None, 1)]),
    ("TRUE", [Token(T.IDENTIFIER, "TRUE", None, 1), Token(T.EOF, "", None, 1)]),
    (
        "if(",
        [
            Token(T.IF, "if", None, 1),
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    ('"while"', [Token(T.STRING, '"while"', "while", 1), Token(T.EOF, "", None, 1)]),
    ("// if else", [Token(T.EOF, "", None, 1)]),
]

class TestKeywordTokens(BaseScannerTest):
    cases = {
        "test_single": KEYWORD_SINGLES,
        "test_pairs": KEYWORD_PAIRS,
        "test_sequences": KEYWORD_SEQUENCES,
        "test_edge_cases": KEYWORD_EDGE_CASES,
    }

IDENTIFIER_SINGLES = [
    ("x", [Token(T.IDENTIFIER, "x", None, 1), Token(T.EOF, "", None, 1)]),
    ("foo", [Token(T.IDENTIFIER, "foo", None, 1), Token(T.EOF, "", None, 1)]),
    ("Foo", [Token(T.IDENTIFIER, "Foo", None, 1), Token(T.EOF, "", None, 1)]),
    ("_", [Token(T.IDENTIFIER, "_", None, 1), Token(T.EOF, "", None, 1)]),
    ("_bar", [Token(T.IDENTIFIER, "_bar", None, 1), Token(T.EOF, "", None, 1)]),
    ("x1", [Token(T.IDENTIFIER, "x1", None, 1), Token(T.EOF, "", None, 1)]),
    ("snake_case", [Token(T.IDENTIFIER, "snake_case", None, 1), Token(T.EOF, "", None, 1)]),
    ("camelCase", [Token(T.IDENTIFIER, "camelCase", None, 1), Token(T.EOF, "", None, 1)]),
]

IDENTIFIER_PAIRS = [
    (
        "a b",
        [
            Token(T.IDENTIFIER, "a", None, 1),
            Token(T.IDENTIFIER, "b", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "foo.bar",
        [
            Token(T.IDENTIFIER, "foo", None, 1),
            Token(T.DOT, ".", None, 1),
            Token(T.IDENTIFIER, "bar", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "a\nb",
        [
            Token(T.IDENTIFIER, "a", None, 1),
            Token(T.IDENTIFIER, "b", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
]

IDENTIFIER_SEQUENCES = [
    (
        "var x = 10;",
        [
            Token(T.VAR, "var", None, 1),
            Token(T.IDENTIFIER, "x", None, 1),
            Token(T.EQUAL, "=", None, 1),
            Token(T.NUMBER, "10", 10.0, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "fun add(a, b) { return a + b; }",
        [
            Token(T.FUN, "fun", None, 1),
            Token(T.IDENTIFIER, "add", None, 1),
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.IDENTIFIER, "a", None, 1),
            Token(T.COMMA, ",", None, 1),
            Token(T.IDENTIFIER, "b", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.LEFT_BRACE, "{", None, 1),
            Token(T.RETURN, "return", None, 1),
            Token(T.IDENTIFIER, "a", None, 1),
            Token(T.PLUS, "+", None, 1),
            Token(T.IDENTIFIER, "b", None, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.RIGHT_BRACE, "}", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "if (x >= y) print x;\nelse print y;",
        [
            Token(T.IF, "if", None, 1),
            Token(T.LEFT_PAREN, "(", None, 1),
            Token(T.IDENTIFIER, "x", None, 1),
            Token(T.GREATER_EQUAL, ">=", None, 1),
            Token(T.IDENTIFIER, "y", None, 1),
            Token(T.RIGHT_PAREN, ")", None, 1),
            Token(T.PRINT, "print", None, 1),
            Token(T.IDENTIFIER, "x", None, 1),
            Token(T.SEMICOLON, ";", None, 1),
            Token(T.ELSE, "else", None, 2),
            Token(T.PRINT, "print", None, 2),
            Token(T.IDENTIFIER, "y", None, 2),
            Token(T.SEMICOLON, ";", None, 2),
            Token(T.EOF, "", None, 2),
        ],
    ),
]

IDENTIFIER_EDGE_CASES = [
    (
        "1x",
        [
            Token(T.NUMBER, "1", 1.0, 1),
            Token(T.IDENTIFIER, "x", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    ("__init__", [Token(T.IDENTIFIER, "__init__", None, 1), Token(T.EOF, "", None, 1)]),
    ("a1b2c3", [Token(T.IDENTIFIER, "a1b2c3", None, 1), Token(T.EOF, "", None, 1)]),
    (
        "x-y",
        [
            Token(T.IDENTIFIER, "x", None, 1),
            Token(T.MINUS, "-", None, 1),
            Token(T.IDENTIFIER, "y", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    (
        "x// comment",
        [
            Token(T.IDENTIFIER, "x", None, 1),
            Token(T.EOF, "", None, 1),
        ],
    ),
    ("a" * 1000, [Token(T.IDENTIFIER, "a" * 1000, None, 1), Token(T.EOF, "", None, 1)]),
]

class TestIdentifierTokens(BaseScannerTest):
    cases = {
        "test_single": IDENTIFIER_SINGLES,
        "test_pairs": IDENTIFIER_PAIRS,
        "test_sequences": IDENTIFIER_SEQUENCES,
        "test_edge_cases": IDENTIFIER_EDGE_CASES,
    }