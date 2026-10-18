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
    def toke_type(self) -> TokenType:
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

    def to_string(self) -> str:
        return f"{self.toke_type} {self.lexeme} {self.literal}"
