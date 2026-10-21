from jerison_lang.token_type import TokenType


class Token:
    def __init__(
        self, toke_type: TokenType, lexeme: str, literal: object, line: int
    ) -> None:
        self.__token_type = toke_type
        self.__lexeme = lexeme
        self.__literal = literal
        self.__line = line

    @property
    def token_type(self) -> TokenType:
        return self.__token_type

    @property
    def lexeme(self) -> str:
        return self.__lexeme

    @property
    def literal(self) -> object:
        return self.__literal

    @property
    def line(self) -> int:
        return self.__line

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Token):
        if not isinstance(other, Token):
            return NotImplemented
        return (
            self.token_type == other.token_type
            and self.lexeme == other.lexeme
            and self.literal == other.literal
        )
