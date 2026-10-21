from jerison_lang.token import Token, TokenType

T = TokenType


token = Token(T.RIGHT_BRACE, "{", None, 0)


class TestTokenMethods:
    def test_getters(self):
        assert token.token_type == T.RIGHT_BRACE
        assert token.lexeme == "{"
        assert token.literal == None
        assert token.line == 0

    def test_str_conversion(self):
        assert str(token) == f"{token.token_type} {token.lexeme} {token.literal}"

    def test_equality(self):
        assert token == Token(T.RIGHT_BRACE, "{", None, 0)
        assert token != Token(T.LEFT_PAREN, ")", None, 0)
