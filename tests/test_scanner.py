import pytest

from jerison_lang.scanner import Scanner, Token, TokenType

T = TokenType


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


class TestSingleCharacterTokens:
    @pytest.mark.parametrize(("source", "expected"), SINGLES)
    def test_single(self, source: str, expected: list[Token]):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        valid_line = True
        for token_one, token_two in zip(tokens, expected):
            print(f"{token_one} {token_one.line}// {token_two} {token_two.line}")
            if token_one.line != token_two.line:
                valid_line = False
        assert tokens == expected and valid_line

    @pytest.mark.parametrize(("source", "expected"), PAIRS)
    def test_pairs(self, source: str, expected: list[Token]):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        valid_line = True
        for token_one, token_two in zip(tokens, expected):
            print(f"{token_one} {token_one.line}// {token_two} {token_two.line}")
            if token_one.line != token_two.line:
                valid_line = False
        assert tokens == expected and valid_line

    @pytest.mark.parametrize(("source", "expected"), SEQUENCES)
    def test_sequences(self, source: str, expected: list[Token]):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        valid_line = True
        for token_one, token_two in zip(tokens, expected):
            print(f"{token_one} {token_one.line}// {token_two} {token_two.line}")
            if token_one.line != token_two.line:
                valid_line = False
        assert tokens == expected and valid_line

    @pytest.mark.parametrize(("source", "expected"), EDGE_CASES)
    def test_edge_cases(self, source: str, expected: list[Token]):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        valid_line = True
        for token_one, token_two in zip(tokens, expected):
            print(f"{token_one} {token_one.line}// {token_two} {token_two.line}")
            if token_one.line != token_two.line:
                valid_line = False
        assert tokens == expected and valid_line
